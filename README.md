# minimal-web-application
This repository contains a minimal fast-api backend and streamlit web frontend, all packaged together using docker
- The folder comprises of three contents:
    - `url-shortener` folder: This is the main backend application, developed with [FASTApi](https://fastapi.tiangolo.com/) that takes a URL and returns a shortened one.
    - `frontend-application` folder: This is the web-ui, made in [streamlit](https://streamlit.io/), that interacts with the backend ui in a userfriendly manner
    - `docker-compose.yaml` file: The docker-compose file for the application suite, to run everything with one command.
- To successfully run this application, you need to have `docker` and `docker-compose` installed and running on your system.
- I managed to complete the bonus part, and the backend is comprised of a `FASTAPI` based application as well as `MongoDB` as persistence store.
- The `url-shortener` and the `frontend-application` as well as a `mongodb` instance can be launched via the `docker-compose.yaml` file. 
- Please go to the folder with the `docker-compose` file and run:

    ```bash
    docker-compose up
    ```
- The frontend application can then be accessed at `http://localhost:8051`
- The backend api can be viewed for its docs at swagger page via `http://localhost:5000/docs`
- The unit-tests can be executed in a new terminal windown on the running api container via:

    ```bash
    docker exec -it api pytest
    ```
- All python applications have a `Dockerfile` to package all the requirements in a single executable environment.s
- The requirements are all pinned in a `requirements.txt` file for a deterministic runtime environment.
- All functions and their parameters are well documented using `docstrings`.
- The formatting of code across repos have been managed by `black`.
- My runtime was Python `3.9.12`.