# Images App

This is a REST API application which allows upload and manage images. Uploaded images might be resized to the provided dimensions.

## Requirements:

- `docker` and `docker-compose` services  
  **Note:** _For development purposes, there is also required **Python** in >= 3.9 version. Preferable also **virtual environment manager** (eg. miniconda3)_

## Running:

1. Clone repository to your local machine.
1. Open terminal and exec command `make run`.  
   **Note:** _App runs on default port `8000`_

## Usage:

- API documentation in available under `/swagger` endpoint. It is also possible to send example requests via swagger (after earlier authorization)
- App has default Django admin panel under `/admin` endpoint

## Configuration:

- there is required to create superuser  
  **Hint:** Type in your terminal, in the repository directory `make superuser`
- superuser can create users
- users can obtain authorization **Bearer** token by sending POST request on `/token` endpoint with `username` and `password` in body

## Development:

- App is covered by unit tests
- To run tests type in the terminal `make test`
