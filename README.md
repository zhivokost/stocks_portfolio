# STOCKS PORTFOLIO PROJECT

python manage.py runserver
python manage.py makemigrations
python manage.py migrate

python manage.py test .

coverage run --source='.' manage.py test .
coverage report
coverage html



