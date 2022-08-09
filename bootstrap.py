import os
import database as _database
import services as _services
import models as _models
from setup_guardians import parse_guardians_csv

if os.path.exists("db.db"):
    os.remove("db.db")

_database.create_db()

db = _services.get_db()
db.query(_models.GuardianModel).delete()
db.commit()

parse_guardians_csv(db)
