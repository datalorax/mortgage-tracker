# Mortgage Refi Tracker

A small Python tool that checks whether refinancing your mortgage is actually worth it — using **lifetime interest cost** as the deciding factor, not just monthly payment.

## Why lifetime interest, not monthly payment?

Refinancing into a new 30-year term almost always lowers your monthly payment, even at a similar or slightly better rate — because you're spreading the balance over 30 fresh years instead of however many you have left. That can look like a win while actually costing you more in total interest over the life of the loan, especially if you're several years into your current mortgage already.

This tool computes both, but the recommendation is gated on lifetime interest: **a refi is only recommended if it saves money over the life of the loan.** A lower monthly payment alone isn't enough — unless you flag that your finances have changed and you need the lower payment regardless of long-term cost.

## How it works

1. **Your original loan terms** (origination date, original rate, original amount, original term) are entered once via a setup script.
2. Your **current balance and remaining term are computed live** from those terms — no need to log into your loan servicer or re-enter numbers every time you check.
3. The **current market rate** is pulled live from FRED's public feed of Freddie Mac's weekly Primary Mortgage Market Survey (PMMS) — no API key required.
4. The tool compares your current loan against a hypothetical refi at today's market rate and tells you: monthly savings, lifetime interest difference, and a recommendation.

This only works for **fixed-rate mortgages** — the math assumes your rate never changes, which isn't true for ARMs.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python.

```bash
git clone <this-repo-url>
cd mortgage-tracker
uv sync
```

Enter your loan's original terms (one-time, or again later if your terms genuinely change — e.g. after an actual refi):

```bash
uv run setup_data.py
```

You'll be prompted for:
- Origination date
- Original interest rate
- Original loan amount
- Original loan term (years)

This writes `mortgage_data.env` — a local file that is **gitignored** and never committed. Your numbers stay on your machine.

## Running a check

```bash
uv run main.py
```

This prints the current market rate, whether a refi is recommended, and the full breakdown (monthly payment comparison, lifetime interest difference, breakeven point in months).

## Assumptions and limits

- Assumes a fixed-rate loan.
- Assumes a new refi would be a fresh 30-year term.
- Closing costs are estimated as a percentage of loan balance (`CLOSING_COST_PERCENT` in `config.py`, default 2.5%) rather than a real quote — adjust if you have an actual estimate.
- Remaining balance is computed from calendar months since origination, assuming on-schedule payments. If you've made extra principal payments or missed any, the computed balance will drift from your real one.

## Using this yourself

This repo is designed to be forked. If you want to run your own copy:

1. Fork the repo.
2. Run `uv run setup_data.py` locally with your own loan details — this only ever writes to your local `mortgage_data.env`, which is gitignored, so your numbers never touch your fork's git history.
3. Adjust `CLOSING_COST_PERCENT` in `config.py` if you have a better estimate than the 2.5% default.

No part of this tool requires paid services — the rate data source (FRED) and the hosting (if you set up scheduled runs via GitHub Actions) are both free.

## Roadmap
- Historical rate/verdict logging to track trends over time
- Home/auto insurance comparison tracking