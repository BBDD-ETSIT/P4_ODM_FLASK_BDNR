from flask import url_for
from run import db


class Hospital(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    city = db.StringField(required=True)

class Patient(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    dni = db.StringField(required=True)
    hospital = db.ReferenceField(Hospital)
    doctors = db.ListField(db.ReferenceField("Doctor")) 

class Doctor(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    speciality = db.StringField(required=True)