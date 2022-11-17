# user-management

## Installation

After created and activated virtual environment install requirements `pip3 install -r requirements.txt`

in file env_file insert long alphanumerical key for JWT_SECRET_KEY, otherwise it will use the flask secret key by default

## RUN

To run type ```docker-compose up --build ```

## Read the tables

To read the tables in the database inside docker: `psql -U db`