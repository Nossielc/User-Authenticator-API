# User-Authenticator-API
In this project, with Python and Bottle, an API was built that makes a CRUD of a user authenticator with a role system.

# Data Structure
Data is persisted in a JSON file, for validation only. But you can easily switch to any database. This file can found in '/src/data/data.json'.
Each user has a username and password. Also, your roles.

# API Endpoints
For all this operations you need to do the login and are authenticated; The program check that.

### POST Operations
(You need to pass a valid palyoad in all the post operations to work properly)

"/api/login" -> Try execute the login checking the credentials, if the credentials is valid set the authentication cookies on the web browser.

"/api/user" -> Insert a new user

"/api/user/<id:int>/role" -> Insert a new type of user Role

### GET Operations
"/api/user" -> Get all the users on the DB

"/api/user/<id:int>" -> Search for a user by ID

"/api/user/<id:int>/role" -> Check all roles for a specific user by ID

### PUT Operations
"/api/user/<id:int>" => Update information for a specific user by ID.

### DELETE Operations
"/api/user/<id:int>" -> Delete an user by ID

"/api/user/<id:int>/role/<role_num:int>" -> Delete one Role for an User. By User ID and Role Number.
