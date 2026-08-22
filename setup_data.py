# setup_data.py
"""
Run this once when you first set up (or if your loan terms change,
e.g. after an actual refi). Everything else is computed live.
Usage: uv run setup_data.py
"""

ENV_FILE = "mortgage_data.env"


def write_current_mortgage_data():
    print("Enter your original mortgage details:\n")

    origination_date = input("Origination date (YYYY-MM-DD): ")
    original_rate_input = input("Original interest rate, as a percent (e.g. 6.25): ")
    original_amount_input = input("Original loan amount, in dollars (e.g. 480000): ")
    original_term_input = input("Original loan term, in years (default 30): ") or "30"

    original_rate_decimal = float(original_rate_input) / 100

    with open(ENV_FILE, "w") as f:
        f.write(f"ORIGINATION_DATE={origination_date}\n")
        f.write(f"ORIGINAL_RATE={original_rate_decimal}\n")
        f.write(f"ORIGINAL_LOAN_AMOUNT={original_amount_input}\n")
        f.write(f"ORIGINAL_TERM_YEARS={original_term_input}\n")

    print(f"\nSaved to {ENV_FILE}.")
    print("Run `uv run main.py` any time — balance and remaining term are computed live.")


if __name__ == "__main__":
    write_current_mortgage_data()