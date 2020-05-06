prod:
	docker-compose -f production.yml up --build --force-recreate -d

prod-proxy:
	docker-compose -f proxy.yml up --build --force-recreate -d

down:
	docker-compose -f production.yml down

local:
	docker-compose -f local.yml up --build

migrations:
	docker-compose -f local.yml -f local-migrations.yml up --build

reset-local:
	docker-compose -f local.yml down -v

test:
	docker-compose -f local.yml -f local-test.yml run --rm django pytest --cov
	docker-compose -f local.yml -f local-test.yml run django mypy {{ cookiecutter.project_slug }}
	docker-compose -f local.yml -f local-test.yml run django coverage html
	docker-compose -f local.yml -f local-test.yml run django flake8 {{ cookiecutter.project_slug }}
