# 002: The repo that grows every day

**Division:** Pkomm Motors
**Domain:** Storage and cost
**Level:** 1
**Status:** Open

## Where I've seen this on the job
On the job, data lands in S3 or ADLS and loads into Snowflake from there. The code repo only ever holds code. This problem moves Pkomm Motors to the same split.

## The ticket
Cloning the Pkomm Motors repo gets slower every week, and most commits say Auto refresh data.

## What is actually wrong
A daily GitHub Action used to commit the full `pkomm_motors.duckdb` file and all raw CSVs. Git keeps every old copy forever. 208 of the first 241 commits came from that bot. The bot is switched off now, but the database and CSVs are still committed, and every old copy is still in the history.

## Why it matters
Git is for code, not for data. In a real company this is the same mistake as storing the warehouse in the code repo.

## The fix (plan)
1. Store the database and raw files outside git (a release asset, object storage, or rebuild on deploy).
2. Stop the bot commits. Done when the project moved into this repo.
3. Point the Streamlit dashboard at the new location.

## On AWS and Azure
Data goes to S3 or ADLS Gen2. The code repo only holds code.

## Write-up
To do.
