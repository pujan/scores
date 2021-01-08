# Scores

## Create environment

```sh
docker-compose build
docker-compose up db
```

In other terminal

```sh
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
```

Press Ctrl+C and stop `db` container, then run all containers:

```sh
docker-compose up
```

Add kinds for example: 'Hokej na lodzie' and 'Piłka nożna' in CMS Admin -> Teams -> Rodzaje.

More information in documentation `doc/doc.pdf`.
