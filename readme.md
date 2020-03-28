# docker start

docker-compose up

# docker dev start

USER_UID=`id -u` USER_GID=`id -g` docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# create fresh db
docker exec -it ziggurat_cms_web_1 ziggurat_cms_db_migrate config.ini
# populate with basic entries
docker exec -it ziggurat_cms_web_1 ziggurat_cms_db_initialize config.ini
