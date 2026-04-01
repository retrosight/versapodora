import numpy as np

# Mortgage details
loan_amount = 370000  # Initial loan balance
annual_interest_rate = 0.02875  # Example interest rate (7%)
monthly_interest_rate = annual_interest_rate / 12
daily_interest_rate = annual_interest_rate / 365
loan_term_years = 30
months = loan_term_years * 12

# Regular monthly mortgage payment
monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** months) / ((1 + monthly_interest_rate) ** months - 1)

# Function to simulate the mortgage with extra payments
def simulate_mortgage(extra_payment_schedule):
    balance = loan_amount
    total_interest_paid = 0
    month = 0

    while balance > 0 and month < months:
        for day in range(30):  # Simplified 30-day month
            daily_extra = extra_payment_schedule(day)
            balance -= daily_extra
            balance = max(balance, 0)
            interest_today = balance * daily_interest_rate
            total_interest_paid += interest_today
            balance += interest_today

        actual_payment = min(monthly_payment, balance)
        balance -= actual_payment
        balance = max(balance, 0)
        month += 1

    return total_interest_paid, month

# Scenario 1: $2,000 extra on the 1st of each month
def early_payment_schedule(day):
    return 2000 if day == 0 else 0

# Scenario 2: $2,000 spread over the month (~$66.67/day)
def daily_payment_schedule(day):
    return 2000 / 30

# Run simulations
interest_early, months_early = simulate_mortgage(early_payment_schedule)
interest_daily, months_daily = simulate_mortgage(daily_payment_schedule)

print(f"Early lump-sum method: ${interest_early:,.2f} in interest, paid off in {months_early} months")
print(f"Daily payment method: ${interest_daily:,.2f} in interest, paid off in {months_daily} months")
print(f"Regular monthly mortgage payment: ${monthly_payment:,.2f}")
