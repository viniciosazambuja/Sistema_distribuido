# Distributed Content Locator

## Introduction

This is a simple tool to locate content in a distributed system. It is based on a simple idea: if tou have a lot of data
distributed in a lot of different node(server + database) and you want to find a specific content. This is a code for init a server to connect to a database and in others nodes. The server allow the user to search a content in the database and in the other nodes. The server is a REST API.

## How to use

### Installation

To install the server you need to install the dependencies with the command:

```bash
pip install typing fastapi pymongo requests json
```

add a settings.json file in the root of the project with the following content:

```json
{
    "id": 1, // the id of the node
    "port": 8001, // the port of the node
    "database": {
        "string": "mongodb://localhost:27017/", // the string to connect to the database
        "name": "node1", // the name of the database
        "collection": "airbnbs" // the name of the collection
    },
    "neighbors": [ 
        {
            "id": 2, // the id of the neighbor node
            "port": 8002 // the port of the neighbor node
        },
        {
            "id": 3, // the id of the neighbor node
            "port": 8003 // the port of the neighbor node   
        }
    ]
}

```

### Run

To run the server you need to run the command:

```bash
python -m uvicorn main:app --reload --port <node_port>
```

### API

The server has the following endpoints:

- GET / - Return the servers settings

- GET /airbnbs/{id} - Return the airbnb with the given id

### Database

Each database needs to have a collection named airbnbs with the following schema:

```json
{
    "id": 1,
    "name": "Name of the airbnb",
}
```
