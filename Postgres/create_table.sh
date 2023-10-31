#!/bin/bash


source ./read_env.sh DB_NAME

# Run:

# SELECT 'CREATE DATABASE mydb'
# WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mydb')\gexec

psql -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || psql -c "CREATE DATABASE $DB_NAME;"

# Executes create_table.sql
psql  -d $DB_NAME -f create_table.sql
