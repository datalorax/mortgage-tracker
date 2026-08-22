# config.py
import os
from datetime import date
from dotenv import load_dotenv

from breakeven import remaining_balance

load_dotenv("mortgage_data.env")

ORIGINATION_DATE = date.fromisoformat(os.environ["ORIGINATION_DATE"])
ORIGINAL_RATE = float(os.environ["ORIGINAL_RATE"])
ORIGINAL_LOAN_AMOUNT = float(os.environ["ORIGINAL_LOAN_AMOUNT"])
ORIGINAL_TERM_YEARS = int(os.environ["ORIGINAL_TERM_YEARS"])

today = date.today()
months_elapsed = (today.year - ORIGINATION_DATE.year) * 12 + (today.month - ORIGINATION_DATE.month)

CURRENT_RATE = ORIGINAL_RATE
LOAN_BALANCE = remaining_balance(
    ORIGINAL_LOAN_AMOUNT, ORIGINAL_RATE, ORIGINAL_TERM_YEARS, months_elapsed
)
REMAINING_TERM_YEARS = ORIGINAL_TERM_YEARS - (months_elapsed / 12)

CLOSING_COST_PERCENT = 0.025
ESTIMATED_CLOSING_COSTS = LOAN_BALANCE * CLOSING_COST_PERCENT