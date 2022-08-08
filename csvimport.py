import datetime
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import db as _database
import models as _models
import schemas as _schemas
import services
import services as _services
import os
import csv
import requests
import shutil
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def parse_guardians_csv(db: _orm.Session):

    with open('Guardians.csv', mode='r') as csv_file:

        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        if not os.path.exists("images"):
            os.makedirs("images")
        if not os.path.exists("images_"):
            os.makedirs("images_")
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            image_url = row["Please provide a profile picture / project logo* *in* SVG *or* PNG format*"]
            if image_url:
                file = image_url.split("/")[-1]
                r = requests.get(image_url, stream=True)

                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True

                    # Open a local file with wb ( write binary ) permission.
                    with open(os.path.join("images_", file), 'wb') as f:
                        shutil.copyfileobj(r.raw, f)

                    filename = os.path.splitext(file)[0]
                    extension = os.path.splitext(file)[1]

                    if extension == ".svg":
                        svg_to_png(file)
                        to_jpgs(f"{filename}.png")
                    else:
                        to_jpgs(file)

                else:
                    print('Image Couldn\'t be retreived')

            guardian_obj = _models.GuardianModel(
                name=row["Full name?"],
                address=row["What's your delegate address / ENS name? "],
                ens=row["What's your delegate address / ENS name? "],
                image_url=image_url,
                reason=row["What are your reasons for wanting to be a delegate?"],
                contribution=row["As a founding Guardian, what was your previous contribution?"],
                start_date=datetime.datetime.now(),
                submit_date=datetime.datetime.now()
            )
            db.add(guardian_obj)
            db.commit()
            db.refresh(guardian_obj)

            print(f'\t{row["Full name?"]}')
            line_count += 1

        print(f'Processed {line_count} lines.')

        # cleanup
        shutil.rmtree("images_")


def svg_to_png(file):
    filename = os.path.splitext(file)[0]
    drawing = svg2rlg(f"images_/{file}")
    renderPM.drawToFile(drawing, f"images_/{filename}.png", fmt='PNG')


def to_jpgs(file):

    filename = os.path.splitext(file)[0]

    im = Image.open(os.path.join("images_", file))

    rgb_im = im.convert('RGB')

    # 3x
    rgb_im.thumbnail((384, 384))
    rgb_im.save(os.path.join("images", f"{filename}_3x.jpg"))

    # 2x
    rgb_im.thumbnail((256, 256))
    rgb_im.save(os.path.join("images", f"{filename}_2x.jpg"))

    # 1x
    rgb_im.thumbnail((128, 128))
    rgb_im.save(os.path.join("images", f"{filename}_1x.jpg"))


async def create_guardian(guardian: _models.GuardianModel):
    guardian_schema = _schemas.Guardian.from_orm(guardian)
    guardian_dict = guardian_schema.dict()
    del guardian_dict["created_at"]


db = next(_services.get_db())
db.query(_models.GuardianModel).delete()
db.commit()


shutil.rmtree("images")
parse_guardians_csv(db)