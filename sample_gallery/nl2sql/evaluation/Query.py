import asyncio
from typing import Tuple, List, Any
from promptflow import tool
from promptflow.connections import CustomConnection
import pyodbc


@tool
def query_to_database(
    sql_groundtruth: str,
    sql_generated: str,
    sqlconn: CustomConnection,
) -> Tuple[List[tuple], List[tuple], bool]:
    result_groundtruth = asyncio.run(get_values(sql_groundtruth, sqlconn))
    result_generated = asyncio.run(get_values(sql_generated, sqlconn))
    value_groundtruth = result_groundtruth[1]
    value_generated = result_generated[1]

    ## if sql_groundtruth includes "order by", set order_by to True, else set it to False
    order_by = "order by" in sql_groundtruth.lower()

    return value_groundtruth, value_generated, order_by


async def get_values(query: str, sqlconn: CustomConnection) -> Tuple[str, Any]:
    print("connecting to database")
    with pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};Server="
        + sqlconn.configs["Server_name"]
        + ";Database="
        + sqlconn.configs["Database_name"]
        + ";Uid="
        + sqlconn.configs["User_name"]
        + ";Pwd="
        + sqlconn.secrets["Password"]
        + ";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;}"
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            results = list(tuple(sorted(row, key=lambda x: str(x))) for row in rows)
    if results is None:
        return "None", None
    else:
        return "Succeed", results
