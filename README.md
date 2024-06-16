# EpidemicSound

## Setup

1. Clone the repository
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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
    uvicorn app.main:app --reload
    ```

## API Endpoints

- `POST /admin/sounds/` - Create a new sound
- `GET /sounds` - Get a list of existing sounds
- `POST /playlists/` - Create a new playlist
- `GET /sounds/recommended` - Get a recommended sound

## Running Tests

1. To run the tests, use:
    ```bash
    pytest
    ```

## Postman Collection

Use the Postman collection provided to test the API.
