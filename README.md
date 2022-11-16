# user-management

## Installation

After created and activated virtual environment install requirements `pip3 install -r requirements.txt`

in file .env insert long alphanumerical keys for SECRET_KEY and JWT_SECRET_KEY

Create an instance of database

```python
flask shell
from src.models.user_db import db
db.create_all()
```

## RUN

To run type `flask run`

To read the tables in the database inside docker: `psql -U db`