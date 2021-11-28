from flask import url_for
from SPARQLWrapper import SPARQLWrapper, JSON

from run import db


class Hospital(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    iri = db.StringField(required=True)
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

def sparql(query, endpoint='http://dbpedia.org/sparql'):
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)
    results = sparql.query().convert()

    print(results)

    info = []

    for result in results["results"]["bindings"]:
        row = {}
        for k, v in result.items():
            row[k] =  v['value']
        info.append(row)
    return info
