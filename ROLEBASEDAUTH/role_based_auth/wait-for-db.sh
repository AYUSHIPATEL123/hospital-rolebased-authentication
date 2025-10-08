#!/bin/sh
# wait-for-db.sh
set -e

host='db'
cmd="$@"

echo "⏳Waiting for MySQL at $host..."

until mysql -h "$host" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e 'SELECT 1' &> /dev/null; do
    >&2 echo "MySQL is unavailable - sleeping" 
    sleep 2
done 

>&2 echo "✅ MySQL is up - executing command"

exec $cmd 