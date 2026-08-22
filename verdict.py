from breakeven import monthly_payment, total_interest

def refi_verdict(
    loan_balance: float,
    current_rate: float,
    new_rate: float,
    remaining_term_years: int,
    closing_costs: float,
    new_term_years: int = 30,
    finances_changed: bool = False,
) -> dict:
    """
    Verdict is driven by lifetime interest, not monthly payment.
    A refi that saves money over the life of the loan is a candidate.
    A refi that costs more in lifetime interest is a non-starter,
    UNLESS finances_changed=True (i.e. you need the lower payment
    regardless of long-run cost) — that's a manual override, since
    only you know when that's true.
    """
    current_payment = monthly_payment(loan_balance, current_rate, remaining_term_years)
    new_payment = monthly_payment(loan_balance, new_rate, new_term_years)
    monthly_savings = current_payment - new_payment

    current_remaining_interest = total_interest(loan_balance, current_rate, remaining_term_years)
    new_total_interest = total_interest(loan_balance, new_rate, new_term_years)
    lifetime_interest_saved = current_remaining_interest - new_total_interest

    saves_lifetime_interest = lifetime_interest_saved > 0

    if saves_lifetime_interest:
        recommend = True
        reason = "Refinancing saves money over the life of the loan."
    elif finances_changed:
        recommend = monthly_savings > 0
        reason = (
            "Costs more in lifetime interest, but flagged as worth considering "
            "since your finances have changed and the lower payment may be needed."
        )
    else:
        recommend = False
        reason = "Costs more in lifetime interest — non-starter under current criteria."

    return {
        "recommend": recommend,
        "reason": reason,
        "lifetime_interest_saved": round(lifetime_interest_saved, 2),
        "monthly_savings": round(monthly_savings, 2),
        "current_payment": round(current_payment, 2),
        "new_payment": round(new_payment, 2),
        "breakeven_months": round(closing_costs / monthly_savings, 1) if monthly_savings > 0 else None,
    }