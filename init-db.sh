#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER SYSTEM SET max_connections = '200';
    ALTER SYSTEM SET shared_buffers = '256MB';
    SELECT pg_reload_conf();
EOSQL
