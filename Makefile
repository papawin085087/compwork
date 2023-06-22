up:
	docker-compose up

run-backend: run-postgres
	docker-compose up -d django celery mail
	bash -c "./scripts/wait-for-it.sh --timeout=0 localhost:8000"
	docker-compose exec django sh -c "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py compilemessages && python manage.py rebuild_department_cache && uvicorn --host 0.0.0.0 --reload configs.asgi:application"

run-postgres:
	docker-compose up -d postgres
	bash -c "./scripts/wait-for-postgres.sh postgres"

run-frontend:
	cd frontend-v2 && ng serve

run-frontend-docker:
	docker-compose up -d angular
	docker-compose exec angular sh -c 'ng serve --host 0.0.0.0'

.migrate:
	docker-compose run --rm app sh -c "python manage.py migrate"

migrate:
	docker-compose run --rm app sh -c "python manage.py migrate" $(filter-out $@,$(MAKECMDGOALS))

.migrations:
	docker-compose run --rm app sh -c "python manage.py makemigrations"

migrations:
	docker-compose run --rm app sh -c "python manage.py makemigrations" $(filter-out $@,$(MAKECMDGOALS))

migrations-migrate: .migrations .migrate

build:
	docker-compose build

build-backend:
	docker-compose build django celery

build-frontend:
	docker-compose exec angular sh -c 'npm install && npm run build:prod'

pip-compile:
	docker-compose run --rm django sh -c "pip install pip-tools && pip-compile"

delete-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

.stop-db-related:
	docker-compose stop django celery

.drop-create-db: run-postgres
	docker-compose exec postgres dropdb -U postgres --if-exists standard
	docker-compose exec postgres createdb -U postgres standard
	docker-compose up -d django celery

.start-db-related:
	docker-compose up -d django celery

reset-db: .stop-db-related .drop-create-db .start-db-related

reset-init-db: reset-db migrations-migrate init-db

reset-migrations: delete-migrations reset-db migrations-migrate

lint:
	docker-compose run --rm app sh -c "python manage.py test && flake8" $(filter-out lint,$(filter-out $@,$(MAKECMDGOALS)))

lint-angular:
	docker-compose exec angular npm run lint -- --quiet

test:
	docker-compose run --rm app sh -c "python manage.py test" $(filter-out test,$(filter-out $@,$(MAKECMDGOALS))) --parallel

test-no-parallel:
	docker-compose run --rm app sh -c "python manage.py test" $(filter-out test,$(filter-out $@,$(MAKECMDGOALS)))

test-np-keep-db:
	docker-compose run --rm app sh -c "python manage.py test" $(filter-out test,$(filter-out $@,$(MAKECMDGOALS))) --keepdb

down:
	docker-compose down --remove-orphans

coverage:
	docker-compose run --rm django sh -c "pip install coverage && coverage run && coverage combine && coverage report -m"

shell:
	docker-compose run --rm app sh -c "python manage.py shell"

init-db:
	docker-compose run --rm django python manage.py init_data --site=1 --host=localhost:8000 group user department group loa memo memo_comment company_configuration theme_configuration upload_memo_type password_policy_setting
	docker-compose run --rm django python manage.py init_data --host=127.0.0.1:8000 group user department group loa memo memo_comment company_configuration theme_configuration upload_memo_type password_policy_setting

show-reverse-url:
	docker-compose exec django python manage.py show_urls

restore-from-dev: stop-quiet reset-db
	echo '- Dumping database from DEV Server'
	docker-compose exec postgres pg_dump --file=/var/lib/postgresql/data/dump.sql --dbname=postgresql://postgres:Codium123!@122.8.155.57:5432/standard
	echo '- Restoring from dump'
	docker-compose exec postgres psql --quiet --file=/var/lib/postgresql/data/dump.sql --username=postgres --dbname=standard
	docker-compose exec postgres rm /var/lib/postgresql/data/dump.sql
	echo '*** Database restoration completed'
	echo '----------------------------------'

bash:
	docker-compose run --rm django sh -c "bash"

message-th:
	docker-compose run --rm django sh -c  "python manage.py makemessages --locale=th"

compile-message:
	docker-compose run --rm django sh -c  "python manage.py compilemessages"

startapp:
	mkdir ./django/apps/$(filter-out $@,$(MAKECMDGOALS))
	docker-compose exec django python manage.py startapp $(filter-out $@,$(MAKECMDGOALS)) apps/$(filter-out $@,$(MAKECMDGOALS))

add-host:
	sudo bash ./scripts/manage-host.sh addhost host.docker.internal 127.0.0.1
