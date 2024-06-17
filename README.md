# EpidemicSound

## Setup

1. Clone the repository (or download from Google Drive)
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

Note: `requirements.txt` was created using `pip freeze`, to make sure that no package would be 
missing from it. This command will capture all installed packages and their versions in the 
requirements.txt file. However, it may include additional packages that were installed but are 
not necessary for this project.

4. Initialize the database:
    ```bash
    alembic upgrade head
    ```
5. Run the application:
    ```bash
    uvicorn app.main:app --reload --port 8080
    ```
Note: You can also run this application in PyCharm. Ensure that you have a Python interpreter 
set up, and you can right-click + select "Run" anywhere in the main.py file.
   
## Overview of the project's structure

- **app/**: Contains all application-related files.
  - main.py: The entry point for the FastAPI application.
  - crud.py: Contains the functions for creating and retrieving data from the database.
  - models.py: Defines the database models using SQLAlchemy.
  - schemas.py: Defines the Pydantic models for request and response validation.
  - database.py: Contains the database connection setup.
  - utils.py: Contains utility functions (e.g., UUID generation).
  - **endpoints/**: Contains the different FastAPI endpoints.
    - admin.py: Endpoints related to admin tasks, here creating sounds.
    - sound.py: Endpoints related to sound management
    - playlist.py: Endpoints related to playlist management.
  - **tests/**: Contains unit tests for the application.
    - test_main.py: Tests for the main application endpoints.
- requirements.txt: Lists the dependencies required for the project.
- README.md: This documentation file.

## API Endpoints

### `POST /admin/sounds/` - Create a new sound (or multiple sounds)

Request Body:

```json
{
    "data": [
        {
        "title": "New song 2",
        "bpm": 120,
        "genres": ["pop"],
        "duration_in_seconds": 130,
        "credits": [
            {
                "name": "King Sis",
                "role": "VOCALIST"
            },
            {
                "name": "Ooyy",
                "role": "PRODUCER"
            }
        ]
        }
    ]
}
```

### `GET /sounds` - Get a list of existing sounds

### `POST /playlists/` - Create a new playlist (or multiple playlists)

Request Body:

```json
{
    "data":
    [
        {
            "title": "New playlist",
            "sounds": ["1d007db5-743c-48e8-a6e7-35c276b69c8c"]
        }
    ]
}
```

### `GET /sounds/recommended?playlistId={playListId}` - Get a recommended sound

## Choices Made
- FastAPI Framework: Chosen for its modern, fast, and efficient capabilities in building APIs.
- SQLAlchemy: Used for ORM to manage database interactions.
- SQLite: Chosen as the database for simplicity and ease of setup. It can be easily switched to 
  another database like PostgreSQL if needed.
- UUIDs: Used for IDs to ensure uniqueness across different tables and to avoid potential 
  conflicts with integer-based IDs.

## Running Tests

- Install Test Dependencies:
Ensure you have pytest installed: `pip install pytest`
- 
- To run the tests, use: `pytest`

## Suggestions for Improvements

### Authentication and Authorization
Implement user authentication and authorization to secure the endpoints.

### Advanced Search and Filtering
Add capabilities to search and filter sounds based on different criteria such as genres, bpm, etc.

### Pagination
Implement pagination for endpoints that return lists of sounds or playlists.

### Enhanced Recommendations
Improve the recommendation algorithm to provide more relevant results based on user preferences 
and listening history.

### Swagger Documentation
Leverage FastAPI’s automatic interactive API documentation (Swagger UI) for better API exploration.

### Error Handling
Improve error handling and validation to provide more informative error messages.

### Deployment
Deploy the application using a cloud service provider like AWS, GCP, or Azure and use a managed database service.

### Environment management
Here `host` and `port` are set as convenient for a local usage. In production, we would set these 
from environment variables. 