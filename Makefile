run:
	python manage.py runserver --settings=cadastro_usuarios_api.local_settings

test:
	python manage.py test apps --pattern="test_*.py" --settings=cadastro_usuarios_api.local_settings

mk:
	python manage.py makemigrations --settings=cadastro_usuarios_api.local_settings

mg:
	python manage.py migrate --settings=cadastro_usuarios_api.local_settings
