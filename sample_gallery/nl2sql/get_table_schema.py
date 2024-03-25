from promptflow import tool
from promptflow.connections import CustomConnection
from langchain.sql_database import SQLDatabase
import ast

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def get_table_schema(tables: str, schema_name: str, sqlconn: CustomConnection) -> str:
    
    tables_list = ast.literal_eval(tables)
    print(tables_list)
    uri = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 17 for SQL Server};Server="+sqlconn.configs['Server_name']+";Database="+sqlconn.configs['Database_name']+";Uid="+sqlconn.configs['User_name']+";Pwd="+sqlconn.secrets['Password']+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;}"   
    #print(uri)
    db = SQLDatabase.from_uri(uri,schema=schema_name, include_tables= tables_list )
        
    return db.get_table_info_no_throw()
