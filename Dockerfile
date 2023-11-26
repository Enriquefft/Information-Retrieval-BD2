# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY /src /app/src/
COPY poetry.lock pyproject.toml /app/
COPY /CSV/spotify_songs.csv /app/CSV/
COPY .env /app/
COPY README.md /app

# Install poetry latest
RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore poetry
RUN poetry config virtualenvs.create false

# Install any needed packages
RUN poetry install --only main --no-interaction --no-ansi

# Run the command to start uWSGI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
