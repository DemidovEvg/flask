#!/bin/sh
# wait-for-postgres.sh

set -e
cmd="$@"
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_SERVICE_NAME -d $POSTGRES_DB -U $POSTGRES_USER -c '\q'; do
>&2 echo $host
>&2 echo $POSTGRES_DB
>&2 echo "Postgres is unavailable - sleeping"
sleep 1
done

>&2 echo "Ща как выполню дальше"
>&2 echo $cmd
exec $cmd