from tapiriik.database import db
import sys
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

# The std_out of this script is intended to be redirected to a file to able it to be a JSON one

# The first arg must be the user ID
user_id = sys.argv[1]

# We try to find it in the mongo database
user = db.users.find_one({"_id": ObjectId(user_id)})

# We formalise a dict for a good data restitution
info = {
    'user':user,
    'connections':[]
}

# We retreive the user's connected services to loop into them.
# Each connected services are then append into the "info" connections array
user_connected_services = user["ConnectedServices"]
for user_connected_service in user_connected_services:
    service_id = user_connected_service["ID"]
    service_info = db.connections.find_one({"_id": ObjectId(service_id)})
    info['connections'].append(service_info)

# In order to convert the "ObjectId" that would not be recognize by json, we first dump :
#   Dict --> BSON
# Then we reload into some kind of BSON dict to redump it into the final JSON form
# It important for lisibility because the json library embed a indent formater that BSON don't
print(json.dumps(json.loads(dumps(info)),indent=4))
