import json

database = {
  "users": {
    "admin" : {
        "username": "admin",
        "password": "admin",
        "access": "All"
    }
  }
}


"""
# Get contents from JSON database
with open(db_name, "r") as json_file:
    current_json = json.load(json_file)
"""

# If "users" dictionary (pseudo table) isn't valid create one 
if "users" not in database:
    database["users"] = {}

# Insert user into JSON database
async def insert_user(username, password):

    if username in database["users"]:
        return (False, "User already exists!")

    database["users"].update(
        { 
            f"{username}" : {
                "username": f"{username}", 
                "password": f"{password}",
                "access": None
            }
        }
    )
    return (True, None)

async def names_and_access():
    return { ( user, database['users'][user]["access"] ) for user in database["users"] }

"""
# Write any updates if there are any to the JSON database
with open(db_name, "w") as new_json:
    json.dump(current_json, new_json, indent=2)
"""