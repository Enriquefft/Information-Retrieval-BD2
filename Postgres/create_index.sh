#!/bin/bash
#
source ./read_env.sh DB_NAME POSTGRES_USER POSTGRES_HOST


# run create_index.sql
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $DB_NAME -f create_index.sql
