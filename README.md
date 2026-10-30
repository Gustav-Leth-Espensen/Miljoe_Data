# Miljoe_Data
Opgave uge 4-8 specialisterne  
Create and ETL pipeline to collect data from DMI's API
and a local API and put it into a PostgreSQL database. 
This pipeline must be able to continuously gather data 
from the two APIs as new data is put into their databases.

# Description
ETL pipeline which can continuously update and put data into postgreSQL database.  
This database is accessible through a local API which continuously update with the new data.

## UML diagram
![Activity diagram]()

# Getting Started
make an .env file with the following variables: 
> DB_USER=user  
> DB_PASSWORD=user_password  
> DB_NAME=database_name
> DB_URL=postgresql://user:user_password@db_server_hostname:5432/database_name  
> API_TOKEN=api_token_from_local_database
 
Make sire this .env is not shared through any version control system.  
In this project the .env file is in the .gitignore file and .dockerignore file.

## Dependencies 
Docker 29.8.1  
requests 2.34.2  
psycopg 3.3.6  
psycopg-binary 3.3.6  
numpy 2.5  
matplotlib.pyplot 3.11

## Executing program
The program can be executed from the terminal using

> docker compose up

our api can be accessed from local host 127.0.0.1:8000


# Authors
Gustav Leth-Espensen
Amalie Fransiska Heugert Mørck

# Version History



