import os
import services as _services
import models as _models
from csvimport import parse_guardians_csv

os.remove("db.db")
_services.create_db()

db = next(_services.get_db())
db.query(_models.GuardianModel).delete()
db.commit()

parse_guardians_csv(db)
