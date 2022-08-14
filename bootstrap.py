import os
import database as _database
import services as _services
from setup_guardians import parse_guardians_csv
from setup_vestings import parse_vestings_csv


if os.path.exists("db.db"):
    os.remove("db.db")

_database.create_db()

db = _services.get_db()

parse_guardians_csv(db)
parse_vestings_csv(db, "user")
parse_vestings_csv(db, "ecosystem")
