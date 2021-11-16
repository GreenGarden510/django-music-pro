import uuid
from mkondo import db

class Configuration(db.Model):
    __tablename__ = 'configurations'

    id = db.Column(db.Integer, primary_key=True)
    configuration_id = db.Column(db.String(50), nullable=False, unique=True)
    key = db.Column(db.String)
    value = db.Column(db.Text)

    def __init__(self, key, value):
        self.configuration_id = uuid.uuid4()
        self.key = key
        self.value = value

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def all(cls):
        # fetch all records
        return cls.query.all()

    @classmethod
    def find(cls, configuration_id):
        # fetch configuration by id
        return  cls.query.filter_by(configuration_id=configuration_id).first()