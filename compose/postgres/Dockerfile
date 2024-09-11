FROM docker.io/postgres:16

COPY ./compose/postgres/maintenance /usr/local/bin/maintenance
RUN chmod +x /usr/local/bin/maintenance/*
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
# COPY ./wait-for-it.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/wait-for-it.sh
# RUN python manage.py migrate