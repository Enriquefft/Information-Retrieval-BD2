# Information-Retrieval-BD2

Search and Information Retrieval system made for the DB2 course.

## Backend

Backend made in FastAPI with a PostgreSQL database.

### Requirements

* Python 3.11.5
* PostgreSQL 13.4

### Setup

1. Create a virtual environment.
```bash
    python3.11 -m venv venv
```

2. Install the dependencies.
```bash
    pip install -r requirements.txt
```

3. Run the server.
```bash
    uvicorn main:app --reload
```

4. Run the tests.
```bash
    python3.11 -m unittest tests/test_*.py
```

### Endpoints

* `/search`
    * `GET` - Returns a list of k documents that match the most the query in descending order of relevance.
    ```bash
    curl -X GET "http://localhost:8000/search?keywords=a&k=10"
    ```

* `/autocomplete`
    * `GET` - Returns a list of possible completions for the query.
    ```bash
    curl -X GET "http://localhost:8000/autocomplete?word=a"
    ```

## Frontend

### Requirements

* Node.js 14.17.6

### Setup

1. Install the dependencies.
```bash
    npm install
```

2. Run the server.
```bash
    npm run dev
```

### Screenshots

![Home](./screenshots/home.png)

![Search](./screenshots/search.png)

![Autocomplete](./screenshots/autocomplete.png)