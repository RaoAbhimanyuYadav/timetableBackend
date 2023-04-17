pip freeze > requirements.txt

# to run

python -m venv env

activate env
-- Window - & ./env/Scripts/Activate.ps1

pip install -r requirements.txt

python manage.py runserver
