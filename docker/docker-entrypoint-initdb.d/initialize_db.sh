#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER test WITH PASSWORD 'test';
    CREATE DATABASE ziggurat_cms;
    GRANT ALL PRIVILEGES ON DATABASE ziggurat_cms TO test;
EOSQL
