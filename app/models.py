from geoalchemy2 import Geometry
from app import db


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phoneFormatted = db.Column(db.String(14))
    phone = db.Column(db.String(10))
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    crossStreet = db.Column(db.String(64))
    postalCode = db.Column(db.String(5))
    state = db.Column(db.String(4))
    geom = db.Column(Geometry('POINT', srid=0))

    @staticmethod
    def add_sweetgreen_geojson_data():
        from sqlalchemy.exc import IntegrityError
        import geojson
        from shapely.geometry import shape

        data = geojson.load(open('sweetgreen.geojson'))
        for feature in data['features']:
            properties = feature['properties']
            print(properties)
            s = Store(**properties)
            geom = feature['geometry']
            s.geom = shape(geom).wkt
            db.session.add(s)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Store {}>'.format(self.id)
