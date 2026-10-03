"""Builds the Kommineni Group website into site/.

Run from the repo root:  python3 tools/build_site.py
Content lives in this file, so every business page stays consistent.

The site is published at pkomm.com/group, inside the pkomm.com portfolio site.
To publish, build straight into the portfolio repo:
    OUT="../pkomm-portfolio/Pkomm Portfolio/group" python3 tools/build_site.py
"""
import hashlib
import math
import os
import re
import shutil
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("OUT", os.path.join(ROOT, "site"))
BRAND = os.path.join(ROOT, "brand")
DOMAIN = "https://pkomm.com"
BASE = "/group"
REPO = "https://github.com/kpk111298/kommineni-group"
PORTFOLIO = "https://pkomm.com"

HONEST = ("Kommineni Group is a simulated company. The businesses, customers and numbers are made up. "
          "The engineering is real: every pipeline, test and fix is built by "
          '<a href="https://pkomm.com">Prameel Kommineni</a>.')

BUSINESSES = [
    {
        "slug": "meel-motors", "name": "Meel Motors", "accent": "#7A2E2A", "live": True,
        "kind": "Car dealership",
        "line": "Five dealerships selling new and used cars, with a service bay at every branch.",
        "intro": ("Meel Motors sells and services cars in Dallas, Chicago, Atlanta, Phoenix and Seattle. "
                  "It was the first Kommineni Group business, and it started life as Kommineni Automotive."),
        "systems": "A dealer management system records every sale, every car on the lot and every service job.",
        "tables": ["Sales", "Vehicles", "Service jobs", "Employees", "Branches and targets"],
        "hard": [
            "Saturdays are the busiest day and month-ends turn frantic as salespeople chase targets.",
            "Illinois bans car sales on Sundays, so the Chicago branch shows no Sunday sales.",
            "Loan rates, gas prices and tax refund season all move what people buy.",
            "Real recalls send waves of owners back to the service bay.",
        ],
        "built": ["Raw data lands in DuckDB, dbt cleans it and builds the business tables",
                  "23 automated data quality tests",
                  "A live dashboard with separate views for executives, branch managers and salespeople"],
        "problems": ["001", "002"],
        "links": [("Open the live dashboard", "https://kommineni-automotive.streamlit.app"),
                  ("See the code", f"{REPO}/tree/main/divisions/meel-motors")],
    },
    {
        "slug": "meel-cart", "name": "Meel Cart", "accent": "#8C5A1E", "live": True,
        "kind": "Online store",
        "line": "The group's online store, selling to customers in five countries.",
        "intro": ("Meel Cart sells online across the US, Canada, the UK, Europe and India. "
                  "Orders change status for days after they are placed, which makes its numbers hard to get right."),
        "systems": "A storefront and order system that records customers, orders, payments and shipments.",
        "tables": ["Customers", "Products", "Orders", "Order items", "Payments", "Shipments"],
        "hard": [
            "Payments fail and succeed days later, so yesterday's revenue keeps moving.",
            "Shipments arrive late and orders get returned weeks after delivery.",
            "Prices, taxes and time zones differ by country.",
            "Black Friday brings ten times a normal day's orders.",
        ],
        "built": ["A daily pipeline that loads only what changed",
                  "Late updates handled by keeping the newest version of every record",
                  "A backfill script that safely rebuilds any date range",
                  "A dashboard with daily orders, revenue, payment failures and on-time delivery"],
        "problems": ["003"],
        "links": [("See the code", f"{REPO}/tree/main/divisions/meel-cart")],
    },
    {
        "slug": "meel-care", "name": "Meel Care", "accent": "#2F5D46", "live": False,
        "kind": "Clinics and health plan",
        "line": "Outpatient clinics and a small health plan.",
        "intro": "Meel Care will run clinics and an insurance plan, with patients created by Synthea, the open source patient simulator.",
        "systems": "An electronic health record for visits, labs and prescriptions, plus a claims system.",
        "tables": ["Patients", "Visits", "Lab results", "Prescriptions", "Claims"],
        "hard": [
            "Hospital records arrive as deeply nested FHIR files.",
            "Patient details must be stripped before analysts see the data.",
            "Claims get adjusted weeks after the visit.",
            "The same patient registers at three clinics under three spellings.",
        ],
        "built": [], "problems": [], "links": [],
    },
    {
        "slug": "meel-move", "name": "Meel Move", "accent": "#2A4A73", "live": False,
        "kind": "Logistics",
        "line": "Delivers Meel Cart orders and moves cars between Meel Motors branches.",
        "intro": "Meel Move will run the group's trucks: last-mile deliveries for Meel Cart and car transfers between dealerships.",
        "systems": "A transportation system for shipments and routes, plus live location pings from every truck.",
        "tables": ["Shipments", "Trucks", "Routes", "Location pings"],
        "hard": [
            "Location pings stream in every few seconds and some arrive twice.",
            "Storms close roads and push deliveries back.",
            "On-time rates depend on time zones and holidays.",
        ],
        "built": [], "problems": [], "links": [],
    },
    {
        "slug": "meel-pay", "name": "Meel Pay", "accent": "#4E3A6B", "live": False,
        "kind": "Loans and payments",
        "line": "Car loans for Meel Motors and card payments for Meel Cart.",
        "intro": "Meel Pay will approve car loans and process card payments for the rest of the group.",
        "systems": "A loan system for applications and approvals, and a payment processor for charges and refunds.",
        "tables": ["Loan applications", "Loans", "Payments", "Refunds", "Chargebacks"],
        "hard": [
            "Interest rates from the Federal Reserve change approvals overnight.",
            "Card numbers and identity details must never reach the warehouse unmasked.",
            "Suspicious payments need flagging in seconds, not the next morning.",
        ],
        "built": [], "problems": [], "links": [],
    },
    {
        "slug": "meel-reach", "name": "Meel Reach", "accent": "#8A3A52", "live": False,
        "kind": "Marketing",
        "line": "Campaigns, ads and email for every Kommineni Group business.",
        "intro": "Meel Reach will run marketing for the whole group, from ad campaigns to email and website tracking.",
        "systems": "A marketing platform with an API for campaigns and spend, plus click events from the websites.",
        "tables": ["Campaigns", "Ad spend", "Email sends", "Web clicks"],
        "hard": [
            "The ad platform returns 100 rows at a time and blocks too many requests.",
            "Millions of clicks a day, some counted twice.",
            "Finance and marketing count customers differently.",
        ],
        "built": [], "problems": [], "links": [],
    },
    {
        "slug": "kommineni-hq", "name": "Kommineni HQ", "accent": "#4A4F58", "live": False,
        "kind": "Shared back office",
        "line": "HR, accounting, customer support, supply chain and IT for the whole group.",
        "intro": "Kommineni HQ is the back office every business shares: people, money, support, suppliers and systems.",
        "systems": "An HR system, a general ledger, a help desk, purchasing and server logs.",
        "tables": ["Employees", "Payroll", "General ledger", "Support tickets", "Purchase orders", "Server logs"],
        "hard": [
            "Every business's revenue has to match the ledger at month-end.",
            "People move between businesses and history has to follow them.",
            "Server logs pile up by the million every day.",
        ],
        "built": [], "problems": [], "links": [],
    },
]

PROBLEMS = {
    "001": ("Yesterday's sales changed overnight", "meel-motors", "Incremental loading", "Open",
            "The dealership's history rewrites itself every morning.", "001-history-rewrites-itself"),
    "002": ("The repo that grows every day", "meel-motors", "Storage and cost", "Open",
            "A daily job saves the whole database into git.", "002-database-in-git"),
    "003": ("Late payments flip the revenue number", "meel-cart", "Incremental loading", "Solved, write-up coming",
            "Payments that succeed days later keep changing past revenue.", "003-late-arriving-updates"),
}

ROADMAP = [
    ("Getting data in", ["A supplier adds a new column every month", "An ad platform that rate limits after 50 calls",
                         "An empty file that wipes out yesterday's dashboard", "Copying a whole loans table every night takes four hours"]),
    ("Trusting the numbers", ["Same customer, three emails, two businesses", "Cars sold before they were bought",
                              "Catch bad data before the boss sees it"]),
    ("Modeling", ["A salesperson moves branches and last year's numbers shift", "One sales model across cars and online orders",
                  "Finance and marketing count customers differently"]),
    ("Streaming", ["Track delivery trucks live", "The same click arrives twice", "Flag a suspicious payment within seconds"]),
    ("Running reliably", ["A job fails at step four of six", "Rebuild six months after a bug fix", "Job B starts before job A finishes"]),
    ("Speed and cost", ["The daily sales query takes 20 minutes", "Millions of tiny files", "Cut the warehouse bill in half"]),
    ("Privacy and audit", ["Analysts can see full identity numbers", "A customer asks to be deleted everywhere",
                           "Who changed this number, and when"]),
    ("Healthcare", ["Flatten nested FHIR patient records", "Remove the 18 HIPAA identifiers",
                    "Claims adjusted weeks after the visit"]),
]


def mark_inner(slug, animate):
    raw = open(os.path.join(BRAND, slug, "mark.svg")).read()
    inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", raw.strip())
    inner = re.sub(r"<title>.*?</title>", "", inner)
    if animate:
        first = True

        def ring(m):
            nonlocal first
            cls = "ring-o draw" if first else "draw"
            first = False
            return f'{m.group(0)} pathLength="1" class="{cls}"'
        inner = re.sub(r'<(circle|path|ellipse|rect) fill="none"', ring, inner)
        inner = re.sub(r'<path fill="#0A0D16"', '<path class="fade" fill="#0A0D16"', inner)
    return inner


def family_svg():
    cx, cy, R = 280, 268, 200
    parts = []
    n = len(BUSINESSES)
    for i, b in enumerate(BUSINESSES):
        a = math.radians(-90 + i * 360 / n)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        x1, y1 = cx + 72 * math.cos(a), cy + 72 * math.sin(a)
        x2, y2 = cx + (R - 44) * math.cos(a), cy + (R - 44) * math.sin(a)
        parts.append(f'<line class="tie" pathLength="1" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    for i, b in enumerate(BUSINESSES):
        a = math.radians(-90 + i * 360 / n)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        s = 0.66
        parts.append(
            f'<a href="/{b["slug"]}/" aria-label="{escape(b["name"])}">'
            f'<g transform="translate({x - 60 * s:.1f} {y - 60 * s:.1f}) scale({s})">{mark_inner(b["slug"], True)}</g>'
            f'<text x="{x:.1f}" y="{y + 58:.1f}" text-anchor="middle">{escape(b["name"])}</text></a>')
    s = 1.15
    parts.append(f'<g class="s1" transform="translate({cx - 60 * s:.1f} {cy - 60 * s:.1f}) scale({s})">'
                 f'{mark_inner("kommineni-group", True)}</g>')
    return (f'<svg class="family" viewBox="0 0 560 560" role="img" aria-labelledby="family-t">'
            f'<title id="family-t">Kommineni Group and its seven businesses</title>{"".join(parts)}</svg>')


def page(path, title, desc, body, current=""):
    canon = DOMAIN + BASE + path
    css_v = hashlib.sha1(open(os.path.join(ROOT, "site-src", "site.css"), "rb").read()).hexdigest()[:8]
    nav = [("Businesses", "/#businesses", "businesses"), ("Engineering", "/engineering/", "engineering"),
           ("How it works", "/about/", "about"), ("Prameel Kommineni", PORTFOLIO, "")]
    nav_html = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if k and k == current else ""}>{t}</a>' for t, h, k in nav)
    full_title = title if title == "Kommineni Group" else f"{title} | Kommineni Group"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kommineni Group">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}{BASE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A0D16">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v={css_v}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/brand/kommineni-group.svg" alt="" width="40" height="40"><span>Kommineni Group</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{nav_html}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div>
      <img src="/assets/brand/kommineni-group-lockup-dark.svg" alt="Kommineni Group" width="280" height="64">
      <p>{HONEST}</p>
    </div>
    <ul>
      <li><a href="/#businesses">Our businesses</a></li>
      <li><a href="/engineering/">Engineering problems</a></li>
      <li><a href="/about/">How it works</a></li>
      <li><a href="{REPO}">Code on GitHub</a></li>
      <li><a href="{PORTFOLIO}">Prameel Kommineni</a></li>
    </ul>
    <p class="small">Copyright 2026 Prameel Kommineni. All rights reserved.</p>
  </div>
</footer>
<script>
  (function () {{
    var b = document.querySelector('.nav-toggle'), n = document.getElementById('nav');
    if (!b) return;
    b.addEventListener('click', function () {{
      var open = n.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
      b.textContent = open ? 'Close' : 'Menu';
    }});
  }})();
</script>
</body>
</html>
"""


def problem_rows(nums, show_business=True):
    rows = []
    by_slug = {b["slug"]: b for b in BUSINESSES}
    for n in nums:
        title, slug, domain, status, line, folder = PROBLEMS[n]
        biz = by_slug[slug]["name"]
        bcell = f'<td class="meta"><a href="/{slug}/">{biz}</a></td>' if show_business else ""
        rows.append(f'<tr><td class="num">{n}</td><td class="what"><a href="{REPO}/tree/main/problems/{folder}">{escape(title)}</a>'
                    f'<span>{escape(line)}</span></td>{bcell}<td class="meta">{domain}</td><td class="meta">{status}</td></tr>')
    head_b = "<th>Business</th>" if show_business else ""
    return (f'<table class="ledger"><thead><tr><th>No.</th><th>Problem</th>{head_b}<th>Area</th><th>Status</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def home():
    items = "".join(
        f'<li><a class="biz" href="/{b["slug"]}/"><img src="/assets/brand/{b["slug"]}.svg" alt="" width="56" height="56">'
        f'<h3>{b["name"]}</h3><p>{escape(b["line"])}</p>'
        f'<span class="status{" live" if b["live"] else ""}">{"Running" if b["live"] else "Opening later"}</span></a></li>'
        for b in BUSINESSES)
    body = f"""
<section class="hero hero-home">
  <div class="wrap">
    <div>
      <h1>Seven businesses.<br>One data team.</h1>
      <p class="lede">Kommineni Group sells cars, runs an online store, clinics, deliveries, loans and marketing.
      Every one of those businesses makes messy data, and the data team keeps it honest.</p>
      <p class="honest">None of the businesses are real. The data problems are, and so are the fixes.
      Kommineni Group is where data engineer <a href="{PORTFOLIO}">Prameel Kommineni</a> builds and breaks real pipelines in the open.</p>
    </div>
    {family_svg()}
  </div>
</section>

<section class="section" id="businesses">
  <div class="wrap">
    <div class="section-head">
      <h2>Our businesses</h2>
      <p>Each business runs its own systems, the way real companies grow. They share one customer list, one calendar and the same real world: interest rates, weather, recalls and holidays.</p>
    </div>
    <ul class="businesses">{items}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>From the engineering desk</h2>
      <p>Every problem is logged like a work ticket, fixed with free tools, tested, and written up. <a href="/engineering/">See the full list and what comes next</a>.</p>
    </div>
    {problem_rows(["003", "001", "002"])}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>How a day runs</h2>
      <p>The same loop, every day, for every business. <a href="/about/">Read how it works</a>.</p>
    </div>
    <ol class="steps">
      <li><strong>Set the day</strong><span>A normal Tuesday, or Black Friday, or a storm in Dallas.</span></li>
      <li><strong>Run the business</strong><span>Each business's systems record sales, visits and payments as they happen.</span></li>
      <li><strong>Move the data</strong><span>Pipelines load, clean and test it, layer by layer.</span></li>
      <li><strong>Report</strong><span>Dashboards show each business how the day went.</span></li>
      <li><strong>Fix what broke</strong><span>Wrong numbers become tickets, fixes and write-ups.</span></li>
    </ol>
  </div>
</section>
"""
    return page("/", "Kommineni Group",
                "Kommineni Group is a simulated family of seven businesses where data engineer Prameel Kommineni solves real data problems in the open.",
                body, "home")


def business(b):
    tables = "".join(f"<li>{t}</li>" for t in b["tables"])
    hard = "".join(f"<li>{escape(h)}</li>" for h in b["hard"])
    actions = "".join(
        f'<a class="button{" primary" if i == 0 else ""}" href="{h}">{escape(t)}</a>' for i, (t, h) in enumerate(b["links"]))
    if b["live"]:
        built = "".join(f"<li>{escape(x)}</li>" for x in b["built"])
        status_block = f"""
    <div>
      <h2>What's built so far</h2>
      <ul>{built}</ul>
    </div>"""
        problems = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Problems from {b["name"]}</h2><p>Logged, fixed and written up one at a time.</p></div>
    {problem_rows(b["problems"], show_business=False)}
  </div>
</section>"""
    else:
        status_block = f"""
    <div>
      <h2>Status</h2>
      <p class="planned"><strong>Opening later.</strong> {b["name"]} is planned. Its systems and first problems are on the <a href="/engineering/">engineering roadmap</a>.</p>
    </div>"""
        problems = ""
    body = f"""
<section class="biz-hero" style="--accent: {b["accent"]}">
  <div class="wrap">
    <img src="/assets/brand/{b["slug"]}.svg" alt="" width="148" height="148">
    <div>
      <p class="kicker">{b["kind"]}, a Kommineni Group business</p>
      <h1>{b["name"]}</h1>
      <p class="lede">{escape(b["intro"])}</p>
      {f'<div class="actions">{actions}</div>' if actions else ""}
    </div>
  </div>
</section>

<section class="section" style="--accent: {b["accent"]}">
  <div class="wrap facts">
    <div>
      <h2>How it runs</h2>
      <p>{escape(b["systems"])}</p>
      <ul class="tables" aria-label="Data it creates">{tables}</ul>
    </div>
    <div>
      <h2>What makes its data hard</h2>
      <ul>{hard}</ul>
    </div>{status_block}
  </div>
</section>
{problems}
"""
    return page(f"/{b['slug']}/", b["name"], f"{b['name']}: {b['line']} A Kommineni Group business.", body)


def engineering():
    road = "".join(
        f'<div><h3>{t}</h3><ul>{"".join(f"<li>{escape(x)}</li>" for x in items)}</ul></div>' for t, items in ROADMAP)
    body = f"""
<section class="hero">
  <div class="wrap" style="display:block">
    <h1>Engineering problems</h1>
    <p class="lede">Real data engineering problems, from first-year mistakes to the kind top companies hire for.
    Each one is fixed with free tools that run on a laptop, with a short note on how the same fix looks on AWS and Azure.</p>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Logged so far</h2><p>Each one links to its ticket, code and tests on GitHub.</p></div>
    {problem_rows(["001", "002", "003"])}
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Coming next</h2><p>The roadmap, grouped by what goes wrong. New problems get added as the businesses grow.</p></div>
    <div class="roadmap">{road}</div>
  </div>
</section>
"""
    return page("/engineering/", "Engineering problems",
                "Real data engineering problems from Kommineni Group, solved with free tools and written up.", body, "engineering")


def about():
    body = f"""
<section class="hero">
  <div class="wrap" style="display:block">
    <h1>How it works</h1>
    <p class="lede">A company that only exists to create real data problems, so they can be solved properly and in the open.</p>
  </div>
</section>
<section class="section">
  <div class="wrap prose">
    <h2>Why a whole company</h2>
    <p>Practice projects usually start with clean data and end with a chart. Real jobs don't work that way. Data arrives late, changes after the fact, breaks without warning and has to match across teams. Kommineni Group exists to recreate that, across every kind of business a data engineer might work for.</p>

    <h2>What's real and what isn't</h2>
    <ul>
      <li>The businesses, people and numbers are simulated.</li>
      <li>The world they react to is real: interest rates from the Federal Reserve, gas prices, weather, vehicle recalls and holidays, all from free public sources.</li>
      <li>The engineering is real: source systems, pipelines, tests, dashboards and fixes, all on <a href="{REPO}">GitHub</a>.</li>
    </ul>

    <h2>A day at the company</h2>
    <ol>
      <li>The day gets set: normal, or a scenario like Black Friday, a supplier changing a file format, or a storm closing a branch.</li>
      <li>Each business's systems record activity as it happens, the way real software does.</li>
      <li>Pipelines load the raw data, clean it, test it and build the numbers each business reports on.</li>
      <li>Dashboards show how the day went.</li>
      <li>When a number looks wrong, it becomes a ticket. The fix gets tested and written up.</li>
    </ol>

    <h2>Tools</h2>
    <p>Everything runs for free: Python, Postgres, DuckDB, dbt, Streamlit and GitHub Actions today, with Spark, Delta Lake, Dagster, Kafka-style streaming and Terraform on the way. Every write-up also shows the cloud version:</p>
    <table class="map">
      <thead><tr><th>Job</th><th>Here</th><th>AWS</th><th>Azure</th></tr></thead>
      <tbody>
        <tr><td>Storage</td><td>Local files</td><td>S3</td><td>ADLS Gen2</td></tr>
        <tr><td>Warehouse</td><td>DuckDB, Postgres</td><td>Redshift, Athena</td><td>Synapse, Fabric</td></tr>
        <tr><td>Transforms</td><td>dbt</td><td>dbt, Glue</td><td>dbt, Data Factory</td></tr>
        <tr><td>Scheduling</td><td>GitHub Actions, Dagster</td><td>MWAA, Step Functions</td><td>Data Factory pipelines</td></tr>
        <tr><td>Streaming</td><td>Redpanda</td><td>Kinesis, MSK</td><td>Event Hubs</td></tr>
        <tr><td>Dashboards</td><td>Streamlit</td><td>QuickSight</td><td>Power BI</td></tr>
      </tbody>
    </table>

    <h2>Who runs it</h2>
    <p>Kommineni Group is built by <a href="{PORTFOLIO}">Prameel Kommineni</a>, a data engineer working across AWS, Azure and Snowflake. The name is his family name. The rest is made up.</p>
  </div>
</section>
"""
    return page("/about/", "How it works",
                "How Kommineni Group works: simulated businesses, real world data and real data engineering.", body, "about")


def write(rel, text):
    if rel.endswith(".html"):
        text = re.sub(r'(href|src)="/(?!/)', rf'\1="{BASE}/', text)
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)


def copy_assets():
    src = os.path.join(ROOT, "site-src")
    dest = os.path.join(SITE, "assets")
    os.makedirs(os.path.join(dest, "fonts"), exist_ok=True)
    shutil.copy(os.path.join(src, "site.css"), os.path.join(dest, "site.css"))
    for f in os.listdir(os.path.join(src, "fonts")):
        shutil.copy(os.path.join(src, "fonts", f), os.path.join(dest, "fonts", f))


def copy_brand():
    dest = os.path.join(SITE, "assets", "brand")
    os.makedirs(dest, exist_ok=True)
    for b in ["kommineni-group"] + [x["slug"] for x in BUSINESSES]:
        shutil.copy(os.path.join(BRAND, b, "mark.svg"), os.path.join(dest, f"{b}.svg"))
    shutil.copy(os.path.join(BRAND, "kommineni-group", "lockup-dark.svg"),
                os.path.join(dest, "kommineni-group-lockup-dark.svg"))


def icons():
    k = re.search(r'<path fill="#0A0D16" d="([^"]+)"', open(os.path.join(BRAND, "kommineni-group", "mark.svg")).read()).group(1)
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><circle cx="60" cy="60" r="60" fill="#0A0D16"/>'
           '<circle cx="60" cy="60" r="52" fill="none" stroke="#C9AE72" stroke-width="3"/>'
           f'<g transform="translate(60 60) scale(1.25) translate(-60 -60)"><path fill="#C9AE72" d="{k}"/></g></svg>\n')
    write("assets/favicon.svg", fav)
    try:
        import cairosvg
    except ImportError:
        print("cairosvg not installed, skipping PNG icons")
        return
    cairosvg.svg2png(bytestring=fav.encode(), write_to=os.path.join(SITE, "assets", "apple-touch-icon.png"),
                     output_width=180, output_height=180)
    lock = open(os.path.join(BRAND, "kommineni-group", "lockup-dark.svg")).read()
    inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", lock.strip())
    w = float(re.search(r'viewBox="0 0 ([\d.]+) 120"', lock).group(1))
    s = 1.6
    og = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
          f'<rect width="1200" height="630" fill="#0A0D16"/>'
          f'<g transform="translate({(1200 - w * s) / 2:.1f} {(630 - 120 * s) / 2:.1f}) scale({s})">{inner}</g></svg>')
    cairosvg.svg2png(bytestring=og.encode(), write_to=os.path.join(SITE, "assets", "og.png"))


if __name__ == "__main__":
    copy_assets()
    copy_brand()
    icons()
    write("index.html", home())
    for b in BUSINESSES:
        write(f"{b['slug']}/index.html", business(b))
    write("engineering/index.html", engineering())
    write("about/index.html", about())
    print("site built")
