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
- test@test.com Test1234 (Role Flipper)
- destroyer@test.com Destroy1234 (Role Destroyer)

### Endpoints

GET, POST api/health
returns 200 OK if the server is running

Permission: none

Example response:
'''json
{
  "code": 200,
  "success": true
}
'''

GET api/rooms
returns a list of rooms and their respective things

Permission: None

Example response:
'''json
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
'''


