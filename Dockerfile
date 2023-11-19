# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY /src /app/
COPY poetry.lock pyproject.toml /app/


# Install poetry latest
RUN pip install 'poetry==$POETRY_VERSION'
RUN poetry config virtualenvs.create false

# Install any needed packages specified in requirements.txt
RUN poetry install --no-dev --nointeraction --no-ansi

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the command to start uWSGI
CMD ["uvicorn", "src.main:app"]
