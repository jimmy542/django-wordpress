#!/bin/sh


echo "* * * * * running sync wordpress data'" >> /etc/crontabs/root
crond -l 2 -f > /dev/stdout 2> /dev/stderr & 
python manage.py runcrons