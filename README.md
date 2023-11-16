# Information-Retrieval-BD2

Search and Information Retrieval system made for the DB2 course.

## Introduction

<div style="text-align: justify">
Information retrieval is the process of obtaining information from a collection of documents. The goal of this project is to build a search engine that allows users to search for songs. In the first part of the project, the search engine will be built using the Single Pass In-Memory Indexing technique. The second part of the project deals with data of multiple dimensions and the use of high dimensional indexing techniques. 
</div>

### Objective

* Index documents in secondary memory through the construction of an Inverted Index with the Single Pass In-Memory Indexing technique.

* Retrieve documents from the index using cosine similarity and the TF-IDF weighting scheme.

### Dataset - Spotify Songs

<div style="text-align: justify">
The dataset contains over 18000 Spotify songs along with their lyrics and information about the artist, genre, etc. The dataset is in CSV format and was extrated from <a href="https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs">Kaggle</a>.
</div>

<div style="text-align: justify">
Example of a document and attributes to be indexed:
</div>

```json
{
    "track_name":"Pangarap",
    "track_artist":"Barbie's Cradle",
    "lyrics":"Minsan pa Nang ako'y napalingon Hindi ko alam...",
    "playlist_genre":"rock",
    "playlist_subgenre":"classic rock"
}
```

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