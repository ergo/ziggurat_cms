# create fresh db
docker exec -it ziggurat_cms_web_1 ziggurat_cms_db_migrate config.ini
# populate with basic entries
docker exec -it ziggurat_cms_web_1 ziggurat_cms_db_initialize config.ini
