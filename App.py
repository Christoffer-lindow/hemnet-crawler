import json
import datetime
from dotenv import dotenv_values
import db
from sqlalchemy.orm import sessionmaker

data = []
config = dotenv_values(".env")
data_base = db.initialize_db(config["CONNECTION_STRING"])
Session = sessionmaker(bind=data_base)
session = Session()
with open("data.json") as f:
    data = json.load(f)

db.Property.__table__.create(bind=data_base, checkfirst=True)
for entity in data:
    property = db.Property()
    if entity.get("url") is not None:
        property.url = entity["url"]
    if entity.get("img-url") is not None:
        property.img_url = entity["img-url"]
    if entity.get("street") is not None:
        property.street = entity["street"]
    if entity.get("address") is not None:
        property.address = entity["address"]
    if entity.get("price") is not None:
        property.price = entity["price"]
    if entity.get("Bostadstyp") is not None:
        property.type = entity["Bostadstyp"]
    if entity.get("Uppl\u00e5telseform") is not None:
        property.contract_type = entity["Uppl\u00e5telseform"]
    if entity.get("Antal rum") is not None:
        property.rooms = entity["Antal rum"][0]
    if entity.get("Boarea") is not None:
         property.area = float(entity["Boarea"].replace(",","."))
    if entity.get("Bygg\u00e5r") is not None:
        property.year_built = datetime.date(int(entity.get("Bygg\u00e5r")[:4]),1,1)
    if entity.get("Avgift") is not None:
        property.rent = entity["Avgift"]
    if entity.get("Pris/m\u00b2") is not None:
        property.price_sqm = float(entity.get("Pris/m\u00b2").replace(",","."))
    if entity.get("Driftkostnad") is not None:
        property.consumption_price = float(entity.get("Driftkostnad").replace(",","."))
    if entity.get("Balkong") is not None:
        if entity.get("Balkong") == "Ja":
            property.balcony = True
        else: 
            property.balcony = False

    session.add(property)
    session.commit()




