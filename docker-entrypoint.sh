#!/bin/bash
set -e

# change the app uid to ones set from environment
if [ -n "${USER_UID}" ]; then
  usermod -u $USER_UID application
fi
if [ -n "${USER_GID}" ]; then
  groupmod -g $USER_GID application
fi

if [ ! -f /opt/rundir/config.ini ]; then
  set +e
  gosu application cp /opt/application/development.ini /opt/rundir/config.ini
  set -e
fi

process_init_files() {
	local f
	for f; do
		case "$f" in
			*.sh)
				# https://github.com/docker-library/postgres/issues/450#issuecomment-393167936
				# https://github.com/docker-library/postgres/pull/452
				if [ -x "$f" ]; then
					echo "$0: running $f"
					"$f"
				else
					echo "$0: sourcing $f"
					. "$f"
				fi
				;;
			*)        echo "$0: ignoring $f" ;;
		esac
	done
}

process_init_files /opt/entrypoint.d/*

if ! [ -z "$SQLALCHEMY_URL" ]
then
    # Backslash-escape the forward slashes in your replacement string, using pattern substitution parameter expansion.
    # Forward slashes also need to be escaped for Bash.
    replacementVar="${SQLALCHEMY_URL//\//\\/}"
    sed -i "s/sqlalchemy.url.*/sqlalchemy.url = ${replacementVar}/" /opt/rundir/config.ini
fi

if ! [ -z "$REDIS_DOGPILE_URL" ]
then
    replacementVar="${REDIS_DOGPILE_URL//\//\\/}"
    sed -i "s/redis.dogpile.url.*/redis.dogpile.url = ${replacementVar}/" /opt/rundir/config.ini
fi

if ! [ -z "$REDIS_SESSIONS_URL" ]
then
    replacementVar="${REDIS_SESSIONS_URL//\//\\/}"
    sed -i "s/redis.sessions.url.*/redis.sessions.url = ${replacementVar}/" /opt/rundir/config.ini
fi

if ! [ -z "$CELERY_BROKER_URL" ]
then
    replacementVar="${CELERY_BROKER_URL//\//\\/}"
    sed -i "s/celery.broker_url.*/celery.broker_url = ${replacementVar}/" /opt/rundir/config.ini
fi

gosu application "$@"
