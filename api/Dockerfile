# Dockerfile for api service
FROM python:3.10.12-slim-bullseye as base

# Define a build argument named PROJECT with a default value of 'api'.
ARG PROJECT=api

# Create a non-root user to run the app with.
RUN groupadd --gid 1000 user && adduser --disabled-password --gecos '' --uid 1000 --gid 1000 user

# Set the working directory for the subsequent commands.
WORKDIR /home/user

# Switch to the non-root user for security purposes.
USER user

# Create a new stage named 'dev' based on the 'base' stage.
FROM base as dev

USER root
# Copy the requirements.txt file and install the Python dependencies.
COPY --chown=user:user ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container.
COPY --chown=user:user ./$PROJECT /home/user/$PROJECT

# Copy the .env file into the container.
COPY --chown=user:user .env /home/user/.env

# Switch back to the non-root user
USER user

# Define the command to run when the container starts.
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload", "--env-file", "/home/user/.env"]

# Create a new stage named 'test' based on the 'base' stage.
FROM base as test

# Copy the requirements.txt file and install the Python dependencies.
COPY --chown=user:user ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER root
# Copy the project files into the container.
COPY --chown=user:user ./$PROJECT /home/user/$PROJECT
# Create a directory for mypy cache and change its ownership to the non-root user.
RUN mkdir /home/user/.mypy_cache && chown user:user -R /home/user/.mypy_cache
# Install pytest within the test stage
RUN pip install pytest

# Define the default command to run when the container starts in the test stage
CMD ["pytest"]
# Switch back to the non-root user
USER user

# Set the default target stage to 'dev'.
FROM dev