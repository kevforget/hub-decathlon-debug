# hub-decathlon-debug
All debug conviniences for the hub-decathlon

## get_dbg_info.py
This permit to retreive some info about an user and its connections thanks to its "_id"
The usage is :
```bash
python[3] get_dbg_info.py [user _id]
```
Or for container use :

```bash
docker exec -it [name_of_the_web_container] python[3] ./get_dbg_info.py [user _id]
```

## fix_connections.py
This script is intended to be used when for some reasons an user loose his connections in the connections tables but keeps it in his connected services.

It will browse all users and refresh his connected services if it detects lost ones
