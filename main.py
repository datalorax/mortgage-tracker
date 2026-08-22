from config import CURRENT_RATE, LOAN_BALANCE, REMAINING_TERM_YEARS, ESTIMATED_CLOSING_COSTS
from rates import get_current_30yr_rate
from verdict import refi_verdict

def main():
    candidate_new_rate = get_current_30yr_rate()
    print(f"Current market rate (30yr): {candidate_new_rate:.3%}")

    result = refi_verdict(
        loan_balance=LOAN_BALANCE,
        current_rate=CURRENT_RATE,
        new_rate=candidate_new_rate,
        remaining_term_years=REMAINING_TERM_YEARS,
        closing_costs=ESTIMATED_CLOSING_COSTS,
    )

    print("=== Refi Check ===")
    print(f"Recommend refi: {result['recommend']}")
    print(f"Reason: {result['reason']}")
    print(f"Current payment: ${result['current_payment']:,.2f}/mo")
    print(f"New payment:     ${result['new_payment']:,.2f}/mo")
    print(f"Monthly savings: ${result['monthly_savings']:,.2f}")
    print(f"Lifetime interest saved: ${result['lifetime_interest_saved']:,.2f}")
    if result['breakeven_months']:
        print(f"Breakeven: {result['breakeven_months']} months")

if __name__ == "__main__":
    main()