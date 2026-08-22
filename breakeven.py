def monthly_payment(principal: float, annual_rate: float, term_years: int) -> float:
    """Standard fixed-rate mortgage payment formula."""
    if annual_rate == 0:
        return principal / (term_years * 12)
    monthly_rate = annual_rate / 12
    n_payments = term_years * 12
    return principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / (
        (1 + monthly_rate) ** n_payments - 1
    )


def total_interest(principal: float, annual_rate: float, term_years: int) -> float:
    """Total interest paid over the life of the loan."""
    payment = monthly_payment(principal, annual_rate, term_years)
    return (payment * term_years * 12) - principal


def refi_breakeven(
    loan_balance: float,
    current_rate: float,
    new_rate: float,
    remaining_term_years: int,
    closing_costs: float,
    new_term_years: int = 30,
) -> dict:
    """
    Compares staying on the current loan vs refinancing — both monthly
    cash flow and total lifetime interest cost.
    """
    current_payment = monthly_payment(loan_balance, current_rate, remaining_term_years)
    new_payment = monthly_payment(loan_balance, new_rate, new_term_years)
    monthly_savings = current_payment - new_payment

    # Lifetime interest: what's left to pay under each scenario
    current_remaining_interest = total_interest(loan_balance, current_rate, remaining_term_years)
    new_total_interest = total_interest(loan_balance, new_rate, new_term_years)
    lifetime_interest_diff = current_remaining_interest - new_total_interest  # positive = refi saves interest

    result = {
        "monthly_savings": round(monthly_savings, 2),
        "current_payment": round(current_payment, 2),
        "new_payment": round(new_payment, 2),
        "lifetime_interest_saved": round(lifetime_interest_diff, 2),
        "breakeven_months": None,
        "worth_it_monthly": monthly_savings > 0,
        "worth_it_lifetime": lifetime_interest_diff > 0,
    }

    if monthly_savings > 0:
        result["breakeven_months"] = round(closing_costs / monthly_savings, 1)

    return result


def remaining_balance(
    original_principal: float,
    annual_rate: float,
    original_term_years: int,
    payments_made: int,
) -> float:
    """Outstanding balance after a number of payments on a fixed-rate loan."""
    monthly_rate = annual_rate / 12
    total_payments = original_term_years * 12

    if monthly_rate == 0:
        return original_principal * (1 - payments_made / total_payments)

    return original_principal * (
        (1 + monthly_rate) ** total_payments - (1 + monthly_rate) ** payments_made
    ) / ((1 + monthly_rate) ** total_payments - 1)