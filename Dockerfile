# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY /src /app/
COPY poetry.lock pyproject.toml /app/
COPY /CSV/spotify_songs.csv /app

ENV CSV_PATH /app/spotify_songs.csv
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD e2Qx9E3ifEmP2oiaHa4R
ENV POSTGRES_HOST spotifydb.clm9mbbezu5l.us-east-1.rds.amazonaws.com

# Install poetry latest
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry config virtualenvs.create false

# Install any needed packages
RUN /root/.local/bin/poetry install --only main --no-interaction --no-ansi

# Make port 80 available to the world outside this container
# EXPOSE 8001

# Run the command to start uWSGI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
