# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from promptflow import tool
from promptflow.connections import CustomConnection
from langchain.sql_database import SQLDatabase

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

@tool
def get_table_names(schema_name: str,sqlconn: CustomConnection) -> str:
    
    uri = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server="+sqlconn.configs['Server_name']+";Database="+sqlconn.configs['Database_name']+";Uid="+sqlconn.configs['User_name']+";Pwd="+sqlconn.secrets['Password']+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;}"   
    #print(uri)
    db = SQLDatabase.from_uri(uri, schema=schema_name)
        
    return db.get_usable_table_names()