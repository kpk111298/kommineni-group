"""
Runs the Pkomm Motors pipeline on demand, for the "How it runs" tab.

It uses the same code as the repo: the data generator, the bronze loader
and the dbt project. Each run gets its own folder and database in /tmp,
so nothing is saved and visitors never touch each other's data.
"""

import os
import json
import random
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field

import duckdb
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DIVISION = os.path.dirname(HERE)
DBT_DIR = os.path.join(DIVISION, "dbt_project", "pkomm_motors")

sys.path.insert(0, os.path.join(DIVISION, "data_generator"))
sys.path.insert(0, os.path.join(DIVISION, "ingestion"))

import generate_data  # noqa: E402
import ingest_bronze  # noqa: E402

TABLES = {
    "locations": "locations.csv",
    "employees": "employees.csv",
    "vehicles": "vehicles.csv",
    "sales_transactions": "sales_transactions.csv",
    "service_jobs": "service_jobs.csv",
}

# The free server is small. One run at a time keeps memory in check.
_run_lock = threading.Lock()


class PipelineBusy(Exception):
    pass


@dataclass
class Step:
    name: str
    detail: str = ""
    seconds: float = 0.0
    ok: bool = True


@dataclass
class RunResult:
    workdir: str
    db_path: str
    seed: int
    broke_it: bool
    steps: list = field(default_factory=list)
    planted: dict = field(default_factory=dict)
    tests: list = field(default_factory=list)
    health: list = field(default_factory=list)
    finished_at: float = 0.0

    @property
    def tests_failed(self):
        return [t for t in self.tests if t["status"] != "pass"]


# ------------------------------------------------------------
# Break it: plant known problems in the raw files
# ------------------------------------------------------------

def plant_problems(sales, vehicles, rng):
    """Adds the kind of mess real source systems send. Returns the counts."""
    dupes = sales.sample(6, random_state=rng.randint(0, 9999))
    sales = pd.concat([sales, dupes], ignore_index=True)

    neg = sales.sample(4, random_state=rng.randint(0, 9999)).index
    sales.loc[neg, "sale_price"] = -sales.loc[neg, "sale_price"]

    missing = sales.drop(neg).sample(3, random_state=rng.randint(0, 9999)).index
    sales.loc[missing, "employee_id"] = None

    odd = vehicles.sample(2, random_state=rng.randint(0, 9999)).index
    vehicles.loc[odd, "status"] = "SOLD - PENDING"

    planted = {
        "duplicate_sales": 6,
        "negative_prices": 4,
        "missing_employee": 3,
        "bad_vehicle_status": 2,
    }
    return sales, vehicles, planted


# ------------------------------------------------------------
# Data health: what was wrong in raw, and what happened to it
# ------------------------------------------------------------

HEALTH_CHECKS = [
    {
        "key": "duplicate_sales",
        "label": "Duplicate sales",
        "raw": """SELECT COUNT(*) - COUNT(DISTINCT transaction_id)
                  FROM bronze.sales_transactions""",
        "clean": """SELECT COUNT(*) - COUNT(DISTINCT transaction_id)
                    FROM main_silver.stg_sales_transactions""",
        "test": "unique_stg_sales_transactions_transaction_id",
    },
    {
        "key": "negative_prices",
        "label": "Zero or negative prices",
        "raw": "SELECT COUNT(*) FROM bronze.sales_transactions WHERE sale_price <= 0",
        "clean": "SELECT COUNT(*) FROM main_silver.stg_sales_transactions WHERE sale_price <= 0",
        "test": None,
    },
    {
        "key": "missing_employee",
        "label": "Sales with no salesperson",
        "raw": "SELECT COUNT(*) FROM bronze.sales_transactions WHERE employee_id IS NULL",
        "clean": "SELECT COUNT(*) FROM main_silver.stg_sales_transactions WHERE employee_id IS NULL",
        "test": None,
    },
    {
        "key": "bad_vehicle_status",
        "label": "Unknown vehicle status",
        "raw": """SELECT COUNT(*) FROM bronze.vehicles
                  WHERE LOWER(status) NOT IN ('available', 'sold', 'reserved')""",
        "clean": """SELECT COUNT(*) FROM main_silver.stg_vehicles
                    WHERE status NOT IN ('available', 'sold', 'reserved')""",
        "test": "accepted_values_stg_vehicles_status__available__sold__reserved",
    },
]


def check_health(db_path, tests):
    failed_tests = {t["name"] for t in tests if t["status"] != "pass"}
    con = duckdb.connect(db_path, read_only=True)
    rows = []
    for c in HEALTH_CHECKS:
        found = con.execute(c["raw"]).fetchone()[0]
        left = con.execute(c["clean"]).fetchone()[0]
        if found == 0:
            outcome = "None found"
        elif left == 0:
            outcome = "Removed by the cleaning step"
        elif c["test"] and c["test"] in failed_tests:
            outcome = "Got through cleaning, caught by a test"
        else:
            outcome = "Got through unnoticed"
        rows.append({"key": c["key"], "label": c["label"], "found": int(found),
                     "left": int(left), "outcome": outcome})
    con.close()
    return rows


def table_counts(db_path, schema):
    con = duckdb.connect(db_path, read_only=True)
    rows = con.execute(f"""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = '{schema}' ORDER BY table_name
    """).fetchall()
    counts = {t: con.execute(f'SELECT COUNT(*) FROM {schema}."{t}"').fetchone()[0]
              for (t,) in rows}
    con.close()
    return counts


# ------------------------------------------------------------
# dbt
# ------------------------------------------------------------

def _dbt(command, workdir, db_path):
    """Runs dbt in its own process, like a scheduler would, then reads
    run_results.json for what happened to each model or test."""
    target = os.path.join(workdir, "target")
    args = [
        sys.executable, "-c", "from dbt.cli.main import cli; cli()",
        command,
        "--project-dir", DBT_DIR,
        "--profiles-dir", DBT_DIR,
        "--target-path", target,
        "--log-path", os.path.join(workdir, "logs"),
        "--no-use-colors",
    ]
    env = dict(os.environ, PKOMM_MOTORS_DB=db_path, DBT_SEND_ANONYMOUS_USAGE_STATS="false")
    proc = subprocess.run(args, env=env, capture_output=True, text=True, timeout=300)

    results = []
    path = os.path.join(target, "run_results.json")
    if os.path.exists(path):
        with open(path) as f:
            for r in json.load(f)["results"]:
                results.append({
                    "name": r["unique_id"].split(".")[2],
                    "status": r["status"],
                    "seconds": round(r.get("execution_time") or 0, 2),
                    "failures": r.get("failures") or 0,
                })
    return proc.returncode == 0, results


# ------------------------------------------------------------
# The run itself
# ------------------------------------------------------------

def run(seed=None, break_it=False, on_step=None):
    """Generate, load, clean, test, build. Calls on_step(Step) as it goes."""
    if not _run_lock.acquire(blocking=False):
        raise PipelineBusy()

    seed = seed if seed is not None else random.randint(1, 99999)
    workdir = tempfile.mkdtemp(prefix="pkomm_motors_")
    raw_path = os.path.join(workdir, "raw")
    os.makedirs(raw_path)
    db_path = os.path.join(workdir, "pkomm_motors.duckdb")
    result = RunResult(workdir=workdir, db_path=db_path, seed=seed, broke_it=break_it)

    def record(step):
        result.steps.append(step)
        if on_step:
            on_step(step)

    try:
        # 1. Generate a fresh day of business, seeded so it can be replayed
        t0 = time.time()
        # The generator uses three sources of randomness: Python's random,
        # Faker, and numpy (through pandas .sample). Seed all three.
        random.seed(seed)
        np.random.seed(seed)
        generate_data.fake.seed_instance(seed)
        locations = generate_data.generate_locations()
        employees = generate_data.generate_employees()
        vehicles = generate_data.generate_vehicles()
        sales = generate_data.generate_sales(employees, vehicles, days_back=90)
        jobs = generate_data.generate_service_jobs(employees, vehicles, days_back=90)
        total = sum(len(d) for d in (locations, employees, vehicles, sales, jobs))
        record(Step("Generate source data",
                    f"{total:,} rows across 5 tables, seed {seed}", time.time() - t0))

        if break_it:
            t0 = time.time()
            sales, vehicles, result.planted = plant_problems(sales, vehicles, random.Random(seed))
            record(Step("Plant problems",
                        f"{sum(result.planted.values())} bad records slipped into the raw files",
                        time.time() - t0))

        for name, df in [("locations", locations), ("employees", employees),
                         ("vehicles", vehicles), ("sales_transactions", sales),
                         ("service_jobs", jobs)]:
            df.to_csv(os.path.join(raw_path, TABLES[name]), index=False)

        # 2. Load raw files into bronze, exactly as they arrived
        t0 = time.time()
        con = duckdb.connect(db_path)
        ingest_bronze.create_bronze_schema(con)
        loaded = 0
        for table, csv_file in TABLES.items():
            loaded += ingest_bronze.load_table(con, table, csv_file, raw_path=raw_path)
        con.close()
        record(Step("Load raw layer", f"{loaded:,} rows kept exactly as they arrived",
                    time.time() - t0))

        # 3. Clean and build with dbt
        t0 = time.time()
        ok, models = _dbt("run", workdir, db_path)
        built = sum(1 for m in models if m["status"] == "success")
        record(Step("Clean and model with dbt", f"{built} of {len(models)} models built",
                    time.time() - t0, ok))

        # 4. Test
        t0 = time.time()
        _, tests = _dbt("test", workdir, db_path)
        result.tests = tests
        passed = sum(1 for t in tests if t["status"] == "pass")
        record(Step("Run data tests", f"{passed} of {len(tests)} tests passed",
                    time.time() - t0, passed == len(tests)))

        # 5. What the business sees
        t0 = time.time()
        silver = table_counts(db_path, "main_silver")
        gold = table_counts(db_path, "main_gold")
        result.health = check_health(db_path, tests)
        record(Step("Build business tables",
                    f"{len(gold)} tables ready, {sum(silver.values()):,} clean rows underneath",
                    time.time() - t0))
    finally:
        _run_lock.release()

    result.finished_at = time.time()
    return result


def cleanup(result):
    if result and result.workdir.startswith(tempfile.gettempdir()):
        shutil.rmtree(result.workdir, ignore_errors=True)
