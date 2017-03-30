This guide will get you started developing the Retrosheet upload scripts.

# Install Python Dependencies
Create a virtual environment for this project. It should run Python 3.5.1.

We use Pip to manage our Python dependencies. to install the packages you need,
just run:
```
pip install -r requirements-dev.txt
```

# Spin up development database
A Docker-compose file is included for use as an easy development database. To
get started, install Docker and Docker Compose (signing up for the Docker for
Mac beta is recommended). Then type:

```
$ docker-compose up -d db
```

The `-d` flag detaches the container output from the terminal so it runs in the
background.

Create the retrosheet database with:
```
$ mysql -h 127.0.0.1 -P 3306 -uroot -proot -e 'CREATE DATABASE retrosheet_raw'
```

# Run database migrations
We use YoYo to manage our database migrations. To run the latest migrations:
```
$ yoyo apply --database mysql://root@127.0.0.1:3306/retrosheet_raw -p
```

## Create a migration
To create a new migration, just do:
```
$ yoyo new
```

Each step should have _two_ arguments: a query to apply the migration, and a
query to roll it back.

## Production migrations
Migrations to the production database have to go through the SSH proxy. You can
set up an SSH tunnel from the command line with a command like this:
```
$ ssh -f user@52.201.41.65 -L 3000:draftqueens.c3s7xotupned.us-east-1.rds.amazonaws.com:3306 -N
```

This will forward port 3306 of 'draftqueens.c3s7xotupned.us-east-1.rds.amazonaws.com'
(as resolved by the SSH proxy at 52.201.41.65) to port 3000 on your local
machine. Then, run your migrations against localhost:3000.
