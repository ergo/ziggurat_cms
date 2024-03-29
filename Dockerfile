# Use an official Python runtime as a parent image
FROM node:13.8.0-buster-slim AS static
RUN apt-get update && apt-get install -y \
    python3 make build-essential gosu git \
 && rm -rf /var/lib/apt/lists/*

ENV PATH $PATH:env/bin
ENV PYTHON python3
# we do not want node to run as id 1000
RUN groupmod -g 999 node && usermod -u 999 -g 999 node
RUN useradd --create-home application
USER application
COPY --chown=application frontend /opt/frontend
WORKDIR /opt/frontend
ENV FRONTEND_ASSSET_ROOT_DIR /opt/frontend/static_build
RUN cd /opt/frontend/ziggurat_cms_front_admin/static_src; yarn
RUN cd /opt/frontend/ziggurat_cms_front_admin/static_src; yarn build
RUN cd /opt/frontend/ziggurat_cms_front_front/static_src; yarn
RUN cd /opt/frontend/ziggurat_cms_front_front/static_src; yarn build
RUN cd /opt/frontend/ziggurat_cms_template_podswierkiem/static_src; yarn
RUN cd /opt/frontend/ziggurat_cms_template_podswierkiem/static_src; yarn build
# throw away the js container
# Use an official Python runtime as a parent image
FROM python:3.7.6-slim-stretch

RUN apt-get update && apt-get install -y \
    gosu \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory to /opt/application
WORKDIR /opt/application

# create application user
RUN useradd --create-home application

RUN chown -R application /opt/application
RUN mkdir /opt/rundir
RUN chown -R application /opt/rundir
RUN mkdir /opt/venv
RUN chown -R application /opt/venv
RUN mkdir /opt/rundir/static_build
RUN chown -R application /opt/rundir/static_build
# Copy the current directory contents into the container at /opt/application
COPY backend/requirements.txt /tmp/requirements.txt
COPY backend/requirements-dev.txt /tmp/requirements-dev.txt

# change to non-root user
USER application

RUN python -m venv /opt/venv
# Install any needed packages specified in requirements.txt
RUN /opt/venv/bin/pip install --disable-pip-version-check --trusted-host pypi.python.org -r /tmp/requirements.txt --no-cache-dir
# make application scripts visible
ENV PATH $PATH:/opt/venv/bin
ENV APP_ENV production
ENV APP_INI_FILE production.ini
# Copy the current directory contents into the container at /opt/application
COPY --chown=application backend /opt/application
# required to install additional modules
COPY --chown=application frontend /opt/application_frontend
# install the app, admin app and templates
# https://thekev.in/blog/2016-11-18-python-in-docker/index.html
# https://jbhannah.net/articles/python-docker-disappearing-egg-info
ENV PYTHONPATH=/opt/application:/opt/application_frontend/ziggurat_cms_front_admin:/opt/application_frontend/ziggurat_cms_front_front:/opt/application_frontend/ziggurat_cms_template_podswierkiem
RUN cd /opt/venv/; /opt/venv/bin/python /opt/application/setup.py develop
RUN cd /opt/venv/; /opt/venv/bin/python /opt/application_frontend/ziggurat_cms_front_admin/setup.py develop
RUN cd /opt/venv/; /opt/venv/bin/python /opt/application_frontend/ziggurat_cms_front_front/setup.py develop
RUN cd /opt/venv/; /opt/venv/bin/python /opt/application_frontend/ziggurat_cms_template_podswierkiem/setup.py develop
# copy pre-built js
COPY --from=static --chown=application /opt/frontend/static_build /opt/rundir/static
# Make port 6543 available to the world outside this container
EXPOSE 6543
USER root
VOLUME /opt/application
VOLUME /opt/application_frontend
VOLUME /opt/rundir
COPY docker/docker-entrypoint.sh /opt/docker-entrypoint.sh
COPY docker/entrypoint.d /opt/entrypoint.d
WORKDIR /opt/rundir
ENTRYPOINT ["/opt/docker-entrypoint.sh"]
# Run application when the container launches
CMD ["pserve", "/opt/rundir/config.ini"]
