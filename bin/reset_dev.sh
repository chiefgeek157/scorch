#!/bin/bash

while getopts 'h' opt; do
    case "$opt" in
        ?|h)
            echo "Usage: $(basename $0) [-h] [-?] [file]"
            echo "  file contains three lines:"
            echo "    admin username"
            echo "    admin password"
            echo "    admin email"
            echo ""
            echo "If file is not provided, the values for the above will"
            echo "be prompted for."
            exit 0
    esac
done
shift "$(($OPTIND - 1))"
filename="$1"

if [ -n "$filename" ]; then
    echo "Filename provided"
    if [ ! -r "$filename" ]; then
        echo "File $filename is not readable"
        exit 1
    fi
    while [ True ]; do
        read username
        read password
        read email
        break
    done < "$filename"
else
    read -p 'Admin username  : ' username
    read -p 'Admin email     : ' email
    read -sp 'Admin password  : ' password
    read -sp 'Reenter password: ' password2
    if [ "$password" != "$password2" ]l; then
        echo "Passwords do not match"
        exit 1
    fi
fi

echo "Deleting existing migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "Deleting SQLite DB..."
rm db.sqlite3

echo "Recreating migrations..."
python manage.py makemigrations

echo "Executing migrations..."
python manage.py migrate

echo "Creating superuser $username at $email with secret password..."
DJANGO_SUPERUSER_USERNAME="$username" \
DJANGO_SUPERUSER_PASSWORD="$password" \
DJANGO_SUPERUSER_EMAIL="$email" \
python manage.py createsuperuser --noinput