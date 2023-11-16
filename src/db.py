from psycopg2 import connect, extensions
from psycopg2.extensions import connection as con, cursor

from config import DB_HOST, DB_NAME

cursorT = cursor

connection: con = connect(host=DB_HOST, dbname=DB_NAME)
