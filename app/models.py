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
    geom = db.Column(Geometry('POINT', srid=4326))


    @staticmethod
    def add_sweetgreen_geojson_data():
        from geoalchemy2.shape import from_shape
        import geojson
        from shapely.geometry import asShape
        from sqlalchemy.exc import IntegrityError

        data = geojson.load(open('sweetgreen.geojson'))
        for feature in data['features']:
            s = Store(**feature['properties'])
            del feature['properties']
            s.geom = from_shape(asShape(feature))
            db.session.add(s)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Store {}>'.format(self.id)
