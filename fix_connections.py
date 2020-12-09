from tapiriik.database import db
from tapiriik.settings import _GLOBAL_LOGGER, COLOG

# We go through all users in database.
users = db.users.find()
for user in users :

    # We retreive user connected services.
    usr_connected_services = user['ConnectedServices']

    # Then we retreive the names of those user connected services.
    usr_connected_services_names = [service['Service'] for service in usr_connected_services]

    # We now get the connections attached to the user thanks to their IDs.
    usr_connections = [user_connection for user_connection in db.connections.find({
        "_id": {
            "$in": [usr_connected_service["ID"] for usr_connected_service in usr_connected_services]
        }
    })]

    # Then we get their names.
    usr_connections_names = [service['Service'] for service in usr_connections]

    # To determine the "lost services" we make a XOR to exclude the connections that are both present
    # in th user connected services and in the connections.
    usr_lost_svc = [service_name for service_name in list(set(usr_connected_services_names) ^ set(usr_connections_names))]

    # We check if there is at least one lost service to avoid overprocessing and rewriting users that don't need it.
    if len(usr_lost_svc) != 0:
        _GLOBAL_LOGGER.info("Impacted USER : "+COLOG.blue(user))
        _GLOBAL_LOGGER.info("User connected services : \t"+COLOG.cyan(usr_connected_services_names))
        _GLOBAL_LOGGER.info("User connections names : \t"+COLOG.magenta(usr_connections_names))
        _GLOBAL_LOGGER.info("User lost services : \t\t"+COLOG.red(usr_lost_svc))
        _GLOBAL_LOGGER.info(COLOG.yellow("-----------------Creating new connected service object-----------------"))
        # We recreate an user connected services object with the services that are really connected.
        new_usr_connected_services = [
            {
                "Service": usr_connection['Service'], 
                "ID":usr_connection["_id"]
            } for usr_connection in usr_connections
        ]

        _GLOBAL_LOGGER.info(usr_connections_names)

        _GLOBAL_LOGGER.info("Actual user connected service in db : \t"+COLOG.cyan(usr_connected_services))
        _GLOBAL_LOGGER.info("The new one shall look like this : \t"+COLOG.magenta(new_usr_connected_services))
        _GLOBAL_LOGGER.info(COLOG.yellow("-----------------Replacing user connected service by the real ones-----------------"))
        # As mentioned by the logs, we replace the connected services array by the new processed ones.
        user['ConnectedServices'] = new_usr_connected_services
        _GLOBAL_LOGGER.info("User with new connected services : "+COLOG.blue(user))
        # We replace the actual user by a recreating one with good services.
        db.users.update_one({"_id": user["_id"]},{"$set":user})
