# FastAPI Template

**Create a .env file based on .env.dist and make all the necessary customizations.**

### To run the application in a docker container, run the command:
`docker-compose up -d`

> [!NOTE]
> POSTGRES_HOST in the .env file should be named the same as the docker postgres container.
> By default, you're all set. If you will not be changing the container names,
> just remove this parameter from the .env or leave it blank
>

### To run the application without a docker container, complete follow these steps:
1. Install dependencies.

    `poetry install` or `pip install -r requirements.txt`
2. Run application.

    `python3 -m app`
