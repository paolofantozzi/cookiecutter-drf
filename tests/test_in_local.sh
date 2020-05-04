#!/bin/sh
# this is a very simple script that tests the docker configuration for cookiecutter-django
# it is meant to be run from the root directory of the repository, eg:
# sh tests/test_docker.sh

set -o errexit

# install test requirements
pip install -r requirements.txt

# create a cache directory
mkdir -p .cache/docker
cd .cache/docker

# create the project using the default settings in cookiecutter.json
cookiecutter ../../ --no-input --overwrite-if-exists use_docker=y $@
cd my_awesome_project

# docker-compose -f local.yml up --build -d

# run the project's type checks
docker-compose -f local.yml -f local-test.yml run django mypy my_awesome_project || docker-compose -f local.yml -f local-test.yml down -v

# run the project's tests
docker-compose -f local.yml -f local-test.yml run django pytest || docker-compose -f local.yml -f local-test.yml down -v

# return non-zero status code if there are migrations that have not been created
docker-compose -f local.yml -f local-test.yml run django python manage.py makemigrations --dry-run --check || { echo "ERROR: there were changes in the models, but migration listed above have not been created and are not saved in version control"; docker-compose -f local.yml -f local-test.yml down -v; exit 1; }

# Test support for translations
docker-compose -f local.yml -f local-test.yml run django python manage.py makemessages || docker-compose -f local.yml -f local-test.yml down -v

docker-compose -f local.yml -f local-test.yml down -v
