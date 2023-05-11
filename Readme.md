pip freeze > requirements.txt

# to run

python -m venv env

activate env
-- Window - & ./env/Scripts/Activate.ps1

pip install -r requirements.txt

python manage.py runserver

DATA MIGRATION
Remember to off Signal and after migration turn on

python manage.py dumpdata > data.json
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

python manage.py flush

python manage.py loaddata db.json
