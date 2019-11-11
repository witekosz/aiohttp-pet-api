# Pet REST API

### About

##### Tools
- web framework - **aiohttp**
- database - **PostgreSQL 11**
- db connection - **aiopg**, **SQLAlchemy**(core)
- data serialization - **Marshmallow**

### Content

Available endpoints: 
- /**pets** GET, POST - List all pets, create new
    * ?type=type
    * ?shelterId=uuid
- /**pets/{uuid}** GET, PATCH, DELETE - Retrieve, update or delete pet 
- /**shelters** GET, POST - List all shelters, create new
    * ?city=city
- /**shelters/{uuid}** GET - Retrieve shelter details
- /**shelters/{uuid}/pets** GET - List pets from shelter
    * ?type=type

### Running local

Run app by docker compose locally(on Linux):
1. Open terminal
2. Copy git repository
3. Go to the project directory:
    ```sh
    $ cd pet_api
    ```
4. Build images:
    ```sh 
   $ docker-compose build
   ```
5. Run containers:
    ```sh
    $ docker-compose up -d
    ```
6. Create a database:
    ```sh
    $ docker-compose exec a_app python db.py
    ```
7. Load sample data:
    ```sh
    $ docker-compose exec a_app python db_data.py
    ```
7. Run tests:
    ```sh
    $ docker-compose exec a_app pytest
    ```
8. The server should be running on: [localhost:8080](http://localhost:8080/)
