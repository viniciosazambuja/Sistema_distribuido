# Impoer the Union class from typing
from typing import Union

# Import the FastAPI class
from fastapi import FastAPI

# Import the MongoClient class from the pymongo module
from pymongo import MongoClient

#import requests module
import requests

# Import the json module
import json

# Read the neighboards.json file
with open('settings.json') as json_file:

    # Load the neighboards.json file
    settings = json.load(json_file)

    myclient = MongoClient(settings['database']['string'])
    mydb = myclient[settings['database']['name']]
    mycol = mydb["airbnbs"]

    # Create the FastAPI app
    app = FastAPI()

    # Create the root endpoint
    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    
    # Create the airbnbs endpoint
    @app.get("/airbnbs/{id}")
    def read_airbnbs(id: int, visited: Union[str, None] = None):
        print(f"Call to /airbnbs/{id} with visited={visited}")
        foundAirbnb = mycol.find_one({"id": id})
        if foundAirbnb:
            return {
                "airbnb": {
                    "id": foundAirbnb["id"],
                    "name": foundAirbnb["name"],
                },
            }
        else:
            neighbors = settings["neighbors"]
            visitedNeighbors = visited.split(',') if visited else []
            visitedNeighbors.append(str(settings['id']))
            for neighbor in neighbors:
                if str(neighbor["id"]) not in visitedNeighbors:
                    print("neighbor: ", neighbor)
                    visitedNeighbors.append(str(neighbor["id"]))
                    visitedAsString = ','.join(visitedNeighbors)
                    print("visitedAsString: ", visitedAsString)
                    try:
                        query = f"?visited={visitedAsString}" if len(visitedAsString) > 0 else ''
                        response = requests.get(f"http://localhost:{neighbor['port']}/airbnbs/{id}{query}" ).json()
                    except :
                        print("Server not found")
                    if "airbnb" in response:
                        print("response: ", response)
                        return response
            return {"error": "Airbnb not found"}
        