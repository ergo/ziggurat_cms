# docker start

    docker-compose up

# docker dev start

    USER_UID=`id -u` USER_GID=`id -g` docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# create fresh db

    docker exec -it ziggurat_cms_web_1 ziggurat_cms_db_migrate config.ini
    
# populate with basic entries

    docker exec -it ziggurat_cms_web_1 ziggurat_cms_db_initialize config.ini

# using static generators to build assets when required

    docker build -f Dockerfile.static . -t ziggurat_cms_statics
    
    # admin
    docker run -it -v `pwd`"/frontend:/opt/frontend" -v "ziggurat_cms_rundir:/opt/rundir" -e FRONTEND_ASSSET_ROOT_DIR="/opt/rundir/static" -e STATIC_DIR="/opt/frontend/ziggurat_cms_template_podswierkiem/static_src" ziggurat_cms_statics

    # front
    docker run -it -v `pwd`"/frontend:/opt/frontend" -v "ziggurat_cms_rundir:/opt/rundir" -e FRONTEND_ASSSET_ROOT_DIR="/opt/rundir/static" -e STATIC_DIR="/opt/frontend/ziggurat_cms_front_front/static_src" ziggurat_cms_statics
