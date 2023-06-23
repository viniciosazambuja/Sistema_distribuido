from typing import Union
from fastapi import FastAPI
from pymongo import MongoClient
import requests
import json

with open('settings.json') as json_file:
    settings = json.load(json_file)
    myclient = MongoClient(settings['database']['string'])
    mydb = myclient[settings['database']['name']]
    mycol = mydb["airbnbs"]

    app = FastAPI()

    @app.get("/")
    def read_root():
        return settings
    
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
        