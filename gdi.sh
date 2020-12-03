#! bin/Bash

docker exec -it hub-decathlon_web_1 python ./Scripts/get_dbg_info.py $1 > ./Output/user_$1.json