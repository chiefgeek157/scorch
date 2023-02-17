#!/bin/bash

force=false

while getopts 'fh' opt; do
    case "$opt" in
        f)
            echo "Forcing destruction of all migrations and the DB"
            force=true
            ;;

        ?|h)
            echo "Usage: $(basename $0) [-f] [-h|-?] [file]"
            echo ""
            echo "  -f      force a yes answer to the warning prompt"
            echo "  -h|-?   show this message"
            echo ""
            echo "  file contains three lines:"
            echo "    admin username"
            echo "    admin password"
            echo "    admin email"
            echo ""
            echo "If file is not provided, the user will be prompted for the values."
            exit 0
    esac
done
shift "$(($OPTIND - 1))"
filename="$1"

if [ "$force" = false ]; then
    echo "#################################################################"
    echo "####################         WARNING         ####################"
    echo "#################################################################"
    echo ""
    echo "Are you sure you want to delete ALL migrations and the DB?"
    echo "This action CANNOT be undone"
    read -p "DELETE? [y/N] " choice
    if [ "$choice" = "y" -o "$choice" = "Y" ]; then
        force=true
    fi
fi

if [ "$force" = false ]; then
    echo "Aborted with no changes"
    exit 0
fi

if [ -n "$filename" ]; then
    if [ ! -r "$filename" ]; then
        echo "File $filename is not readable"
        exit 1
    fi
    echo "Using superuser credentials from $filename"
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