# NNN: Problem title in plain words

**Division:** Meel ___
**Domain:** ___
**Level:** 1 to 4
**Status:** Open / In progress / Solved / Published

## The everyday version
One short paragraph that explains the problem with something from normal life, before any tech word. A recruiter who has never written SQL should get it. Then one line that maps it back: "That's exactly what happened to Meel Cart's revenue."

Good analogies are things everyone has lived through: a bank statement, a restaurant bill, a package being tracked, a doctor's office, a filing cabinet.

## The problem

### The ticket
What the business person sees. One or two sentences, like a real Slack message.

### What is actually wrong
The root cause, found by looking at the data and the code. Show the query or the rows that prove it.

### Why it matters
Money, trust, time or risk. Use a number if you can.

### Constraints
Free tools only, runs on a laptop, plus any business rule.

## The solution

### 1. The fix in plain words
Three or four sentences anyone on the team could follow. Then the 10 to 15 lines of code that matter, not the whole file, with a link to the full file.

### 2. Why this way
The other options and why they lost. At least two. Example: reload everything daily (gets slower forever), clean duplicates at read time (pushes the problem onto every analyst).

### 3. What went wrong along the way
The bug, wrong turn or surprise you hit while building it, and how you caught it. Link the commit.

### 4. Proof
- A test that fails without the fix and passes with it. Link it.
- Real numbers from running it: rows in, rows changed, time taken, before and after.
- Run it twice and show the result doesn't change.

### 5. Honest limits
Where this fix would break: bigger data, a crash halfway, a new kind of input. And what you'd do next about it.

### 6. On the job: AWS, Azure, Snowflake
| Step | What I used here | AWS | Azure | Snowflake / Databricks |
|---|---|---|---|---|
| | | | | |

Then say it plainly, in four parts: the service a team would use, why I used the open source tool instead, what carries over as is, and what changes in the cloud. See the [tool map](../docs/tool-map.md).

## What I learned
Two or three lines. This becomes the interview answer.

## Write-up
Link to the post on pkomm.com/blog.
