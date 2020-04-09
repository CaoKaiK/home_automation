# Home Automation

This project is part of the Udacity Fullstack Developer Nanodegree. The application comprises a backend using flask and a sqlite database for development and a postgres database for production. The main feature is the RESTful API that allows interaction with the application. The general idea of this app is to model a household with several rooms that each contain several things that the user can activate or deactivate.

## API

### Roles and Permissions
There are three permissions:
- flip:things This permission allows the user to flip the status of a thing from active to inactive and vice versa
- delete:things This permissions allows the user to delete a thing
- delete:rooms This permission allows the user to delete a room

There are two roles:
- Flipper: Users with the flipper have the permission to flip things
- Destroyer: Users with the role destroyer can delete rooms and things, they also inherit the permission of flipping things

### Header
The following header parameters should be set before making a request:
- Content-Type: application/json
- Accept: application/json

- Authorization: Bearer Token

The Token will be provided by logging in with the following test accounts:
- test@test.com 
    PW: Test1234 (Role Flipper)
- destroy@test.com 
    PW: Destroy1234 (Role Destroyer)

### Endpoints

#### GET, POST api/health
returns 200 OK if the server is running

Parameter: none

Body: none

Permission: none

Example response:
```json
{
  "code": 200,
  "success": true
}
```

#### GET api/rooms
returns a list of rooms and their respective things

Parameter: none

Body: none

Permission: None

Example response:
```json
{
  "result": [
    {
      "created_on": "2020-04-08T17:52:51.234417",
      "id": 1,
      "name": "Test Room",
      "things": [
        {
          "id": 1,
          "name": "New Thing 1",
          "status": false
        },
        {
          "id": 2,
          "name": "New Thing 2",
          "status": true
        }
      ],
      "total_things": 2
    },
    {
      "created_on": "2020-04-08T17:52:59.897353",
      "id": 2,
      "name": "Test Room 2",
      "things": [],
      "total_things": 0
    },
    {
      "created_on": "2020-04-08T17:53:06.420439",
      "id": 3,
      "name": "Test Room 3",
      "things": [
        {
          "id": 3,
          "name": "New Thing 3",
          "status": false
        },
        {
          "id": 4,
          "name": "New Thing 4",
          "status": true
        }
      ],
      "total_things": 2
    },
    {
      "created_on": "2020-04-08T18:28:11.568399",
      "id": 4,
      "name": "Very long Room name",
      "things": [],
      "total_things": 0
    }
  ],
  "success": true
}
```

#### POST api/rooms
Creates a room with the requested name.

Parameter: none

Body: "name": "Living Room"

Name must be unique and will be checked.

Permission: none

Example response:
```json
{
  "result": {
    "created_on": "2020-04-09T13:37:51.412626",
    "id": 5,
    "name": "Living Room",
    "things": [],
    "total_things": 0
  },
  "success": true
}
```

#### GET api/rooms/id
Get the information of a room.

Parameter: id

Body: none

Permission: none

Example response:
```json
{
  "result": {
    "created_on": "2020-04-09T13:37:51.412626",
    "id": 5,
    "name": "Living Room",
    "things": [],
    "total_things": 0
  },
  "success": true
}
```

#### PATCH api/rooms/id
Change the name of a room

Parameter: id

Body: "name" : "New Name"

Permission: none

Example response:
```json
{
  "result": {
    "created_on": "2020-04-09T13:37:51.412626",
    "id": 5,
    "name": "New Name",
    "things": [],
    "total_things": 0
  },
  "success": true
}
```

#### DELETE api/rooms/id
Delete a room with room id

Parameter: id = room_id

Body: none

Permission: delete:rooms

Example response:
```json
{
  "result": {
    "created_on": "2020-04-09T13:37:51.412626",
    "id": 5,
    "name": "New Name",
    "things": [],
    "total_things": 0
  },
  "success": true
}
```

#### GET api/things
Get a list of all things or filtered by location

Parameter: room

Body: none

Permission: none

Example response:
api/things?room=1
```json
{
  "result": [
    {
      "created_on": "2020-04-08T17:53:18.692592",
      "id": 1,
      "last_switched": "2020-04-08T20:08:28.641331",
      "location": {
        "id": 1,
        "name": "Test Room"
      },
      "name": "New Thing 1",
      "status": false
    },
    {
      "created_on": "2020-04-08T17:53:24.379036",
      "id": 2,
      "last_switched": "2020-04-08T19:33:27.021741",
      "location": {
        "id": 1,
        "name": "Test Room"
      },
      "name": "New Thing 2",
      "status": true
    }
  ],
  "success": true
}
```

#### POST api/things
Create a thing in a room

Parameter: none

Body: "name": "Thing Name", "room_id": "room_id"

Permission: none

Example response:
```json
{
  "result": {
    "created_on": "2020-04-09T13:47:03.978967",
    "id": 5,
    "last_switched": "2020-04-09T13:47:03.978967",
    "location": {
      "id": 3,
      "name": "Test Room 3"
    },
    "name": "New Thing 4",
    "status": false
  },
  "success": true
}
```

#### GET api/things/id
Get details on a thing

Parameter: none

Body: none

Permission: none

Example response:
```json
{
  "result": {
    "created_on": "2020-04-08T17:53:18.692592",
    "id": 1,
    "last_switched": "2020-04-08T20:08:28.641331",
    "location": {
      "id": 1,
      "name": "Test Room"
    },
    "name": "New Thing 1",
    "status": false
  },
  "success": true
}
```

#### PATCH api/things/id
Rename a thing

Parameter: none

Body: "name": "New Name"

Permission: none

Example response:
```json
{
  "result": {
    "created_on": "2020-04-08T17:53:18.692592",
    "id": 1,
    "last_switched": "2020-04-08T20:08:28.641331",
    "location": {
      "id": 1,
      "name": "Test Room"
    },
    "name": "New Name",
    "status": false
  },
  "success": true
}
```

#### DELETE api/things/id
Delete a thing

Parameter: none

Body: none

Permission: delete:things

Example response:
```json
{
  "message": "Thing New Name was deleted",
  "result": {},
  "success": true
}
```

#### PATCH api/things/id/flip
Flip a thing from on to off and vice versa

Parameter: none

Body: none

Permission: flip:things

Example response:
```json
{
  "result": {
    "created_on": "2020-04-08T17:53:24.379036",
    "id": 2,
    "last_switched": "2020-04-09T13:50:42.820074",
    "location": {
      "id": 1,
      "name": "Test Room"
    },
    "name": "New Thing 2",
    "status": false
  },
  "success": true
}
```
