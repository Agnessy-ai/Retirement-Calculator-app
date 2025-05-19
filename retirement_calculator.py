import pandas as pd

def calculate_future_value(today_value, years, inflation_rate):
    """Compute future value of today's money after accounting for inflation."""
    return today_value * ((1 + inflation_rate) ** years)

def compute_contribution_needed(future_goal, years, investment_rate, tol=1e-2):
    """Use binary search to solve for required annual contribution."""
    low, high = 0, future_goal
    while high - low > tol:
        mid = (low + high) / 2
        future_value = sum(mid * (1 + investment_rate) ** (years - t - 1) for t in range(years))
        if future_value < future_goal:
            low = mid
        else:
            high = mid
    return round(mid, 2)

def create_schedule(contribution, years, rate, start_year):
    """Generate year-by-year contribution and its future value."""
    records = []
    for t in range(years):
        year = start_year + t
        fv = contribution * ((1 + rate) ** (years - t - 1))
        records.append({
            "Year": year,
            "Years to Retirement": years - t,
            "Annual Contribution": f"${contribution:,.2f}",
            "Future Value at Retirement": f"${fv:,.2f}"
        })
    total_fv = sum(contribution * ((1 + rate) ** (years - t - 1)) for t in range(years))
    total_contrib = contribution * years
    records.append({
        "Year": "TOTAL",
        "Years to Retirement": "",
        "Annual Contribution": f"${total_contrib:,.2f}",
        "Future Value at Retirement": f"${total_fv:,.2f}"
    })
    return pd.DataFrame(records)

def smart_retirement_calculator():
    print("💡 Smart Retirement Calculator\n")

    # Get user inputs
    today_goal = float(input("Enter the amount you want in today's dollars (e.g., 1000000): "))
    years = int(input("Enter number of years until retirement (e.g., 40): "))
    inflation_rate = float(input("Enter expected inflation rate (e.g., 0.03 for 3%): "))
    investment_rate = float(input("Enter your investment return rate (e.g., 0.05 for 5%): "))
    start_year = int(input("Enter the current year (e.g., 2024): "))

    # Step 1: Adjust today's goal to future value
    future_goal = calculate_future_value(today_goal, years, inflation_rate)
    print(f"\n🎯 Future Value Needed: ${future_goal:,.2f}")

    # Step 2: Compute required contribution
    annual_contribution = compute_contribution_needed(future_goal, years, investment_rate)
    print(f"💰 Required Annual Contribution: ${annual_contribution:,.2f}")

    # Step 3: Create full schedule
    df = create_schedule(annual_contribution, years, investment_rate, start_year)

    # Display result
    print("\n📅 Retirement Contribution Schedule:\n")
    print(df.to_string(index=False))

    # Optional: Save to Excel
    save = input("\nWould you like to save this to Excel? (y/n): ").lower()
    if save == 'y':
        df.to_excel("retirement_schedule.xlsx", index=False)
        print("✅ File saved as 'retirement_schedule.xlsx'.")

# Run the app
if __name__ == "__main__":
    smart_retirement_calculator()
