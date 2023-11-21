from promptflow import tool

# Specify the type for input1 as a tuple of 8 elements
@tool
def my_python_tool(input1: (str, str, float, str, float, float, str, str)) -> str:
    (
        account_holder_name,
        account_type,
        balance,
        employment_status,
        average_monthly_deposit,
        average_monthly_withdrawal,
        financial_goal,
        risk_tolerance,
    ) = input1

    prompt = f"""Based on the following detailed financial profile, could you provide a comprehensive financial plan? The plan should align with the account holder's long-term goals, risk tolerance, and current financial standing.

    1. **Account Holder:** {account_holder_name}
       - Could you consider personalizing the advice for different age groups or life situations?
       
    2. **Account Type:** {account_type}
       - How does this account type align or conflict with the individual's financial objectives?

    3. **Current Balance:** {balance}
       - Could you outline strategies for maximizing the value of the current balance?

    4. **Employment Status:** {employment_status}
       - How should the employment status factor into savings or investment strategies?

    5. **Average Monthly Deposit:** {average_monthly_deposit}
       - What percentage of the average monthly deposit should go into investments, savings, and emergency funds?

    6. **Average Monthly Withdrawal:** {average_monthly_withdrawal}
       - Can you suggest any methods to minimize unnecessary withdrawals?

    7. **Financial Goal:** {financial_goal}
       - What are the short-term and long-term steps needed to achieve this financial goal?

    8. **Risk Tolerance:** {risk_tolerance}
       - Given the risk tolerance, what kind of investment opportunities should be explored or avoided?

    Please provide a detailed and step-by-step financial plan that addresses these points."""

    return prompt
