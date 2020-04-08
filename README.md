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

GET api/rooms
returns a list of rooms and their respective things




