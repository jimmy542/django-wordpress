#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
python manage.py migrate
# echo "* * * * * echo 'cron job start'" >> /etc/crontabs/root
echo "*/5 * * * * "python /usr/src/app/manage.py runcrons >> /etc/crontabs/root
crond -l 2 -f > /dev/stdout 2> /dev/stderr & 
exec "$@"
