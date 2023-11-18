import os  # Import the os library for environment variables
#import pyodbc  # Import the ODBC library
from promptflow import tool
from promptflow.connections import CustomConnection
from urllib.parse import urlparse
#from azure.cosmos import CosmosClient, PartitionKey, exceptions

@tool
def my_python_tool(account_number: str, connection: CustomConnection) -> str:
    # Set environment variables for ODBC
    os.environ['ODBCINI'] = '/etc/odbc.ini'
    os.environ['ODBCINSTINI'] = '/etc/odbcinst.ini'
    os.environ['ODBCSYSINI'] = '/usr/lib/x86_64-linux-gnu/odbc/'

    host = connection.endpoint
    port = connection.port
    database = connection.database
    user = connection.username
    password = connection.password

    # Initialize the ODBC connection string
    conn_str = "DRIVER=/usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so;" + "SERVER=" + host + ";PORT=" + port + ";DATABASE=" + database + ";UID=" + user + ";PWD=" + password + ";sslmode=require;"

    # Initialize the ODBC connection
    conn = pyodbc.connect(conn_str)

    # Create a cursor object
    cursor = conn.cursor()

    # Issue a query to fetch all 8 columns
    query = f"SELECT account_holder_name, account_type, balance, employment_status, average_monthly_deposit, average_monthly_withdrawal, financial_goal, risk_tolerance FROM bank_accounts WHERE account_number = {account_number}"
    #query = f"SELECT * FROM bank_accounts"
    
    cursor.execute(query)
    result = cursor.fetchone()

    print(result)

    # Initialize variables to None in case no records are found
    account_holder_name = None
    account_type = None
    balance = None
    employment_status = None
    average_monthly_deposit = None
    average_monthly_withdrawal = None
    financial_goal = None
    risk_tolerance = None

    if result:
        # Unpack the result into separate variables
        (
            account_holder_name,
            account_type,
            balance,
            employment_status,
            average_monthly_deposit,
            average_monthly_withdrawal,
            financial_goal,
            risk_tolerance
        ) = result
        
        print(f"Account Holder: {account_holder_name}")
        print(f"Account Type: {account_type}")
        print(f"Balance: {balance}")
        print(f"Employment Status: {employment_status}")
        print(f"Average Monthly Deposit: {average_monthly_deposit}")
        print(f"Average Monthly Withdrawal: {average_monthly_withdrawal}")
        print(f"Financial Goal: {financial_goal}")
        print(f"Risk Tolerance: {risk_tolerance}")
    else:
        print("No records found.")

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return (
        account_holder_name,
        account_type,
        balance,
        employment_status,
        average_monthly_deposit,
        average_monthly_withdrawal,
        financial_goal,
        risk_tolerance
    )

