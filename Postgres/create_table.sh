#!/bin/bash


source ./read_env.sh DB_NAME POSTGRES_USER POSTGRES_HOST

# Run:

# SELECT 'CREATE DATABASE mydb'
# WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mydb')\gexec

psql -h $POSTGRES_HOST -U $POSTGRES_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || psql -h $POSTGRES_HOST -U $POSTGRES_USER -c "CREATE DATABASE $DB_NAME;"


# Executes create_table.sql
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $DB_NAME -f create_table.sql

