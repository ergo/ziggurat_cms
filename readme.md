# docker start
    mkdir rundir
    docker-compose up

# docker dev start

    USER_UID=`id -u` USER_GID=`id -g` docker-compose up

# create fresh db

    docker-compose exec web ziggurat_cms_db_migrate config.ini
    
# populate with basic entries

    docker-compose exec web ziggurat_cms_db_initialize config.ini

# using static generators to build assets when required

    # admin
    docker-compose run statics_admin yarn build

    # front
    docker-compose run statics_front yarn build
