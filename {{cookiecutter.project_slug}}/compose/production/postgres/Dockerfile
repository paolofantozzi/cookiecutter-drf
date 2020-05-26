FROM {% set postgres_version, postgis_version = cookiecutter.postgresql_postgis_version.split('/') %}{% if cookiecutter.use_postgis == 'y' %}postgis/postgis:{{ postgis_version }}{% else %}postgres:{{ postgres_version }}{% endif %}

COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
