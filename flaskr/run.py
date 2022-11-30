from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
import json
import uuid
import os

app = Flask(__name__)
### TAREA: Definir la URI de conexión, porque si no lo especifico se conectará a la bbdd de nombre test
app.config['MONGODB_SETTINGS'] = {}

db = MongoEngine()
db.init_app(app)

from models import Hospital, Patient, Doctor, sparql

@app.route("/")
def index():
    return redirect("/hospitals")

@app.route("/home")
def show_home():
    return redirect("/hospitals")

# Buscar todos los hospitales
@app.route("/hospitals")
def show_hospitals():
    ### TAREA: Complete la función a partir de aquí ###

    return render_template("index_hospitals.html",hospitals=all_hospitals)

# Filtra los hospitales por ciudad
@app.route('/hospitals/filterByCity',methods=['GET','POST'])
def filterHospitalsByCity():
    ### TAREA: Complete la función a partir de aquí ###

    return render_template("index_hospitals.html",hospitals=all_hospitals)

# Buscar pacientes de un hospital ordenadors por el nombre (de la A a la Z)
@app.route('/hospitals/<hospital_id>/patients',methods=['GET'])
def list_hospital_patients(hospital_id):
    ### TAREA: Complete la función a partir de aquí ###

    return render_template("index_patients.html",hospital=hospital_id, patients= patients, patientDeleted='')

# Muestra la informacion de un paciente
@app.route('/hospitals/<hospital_id>/patients/<patient_id>',methods=['GET','POST'])
def read_patient(hospital_id,patient_id):
    ### TAREA: Complete la función a partir de aquí ###

    return render_template("show.html",hospital=hospital_id, patient= patient)

@app.route("/hospitals/<hospital_id>/patients/new")
def show_create(hospital_id):
    return render_template('new.html',hospital=hospital_id)

# Crea un paciente en un hospital
@app.route('/hospitals/<hospital_id>/patients',methods=['POST'])
def create_patient(hospital_id):
    ### TAREA: Complete la función a partir de aquí ###

    return redirect('/hospitals/'+hospital_id+'/patients')

# Obtiene el formulario para actualizar un paciente
@app.route('/hospitals/<hospital_id>/patients/<patient_id>/edit',methods=['GET'])
def create_edited_patient(hospital_id,patient_id):
    patient = Patient.objects.get(id=patient_id)
    return render_template("edit.html",hospital=hospital_id, patient= patient)

# Actualiza un paciente
@app.route('/hospitals/<hospital_id>/patients/<patient_id>/updated', methods = ['POST','PUT'])
def update_patient(hospital_id,patient_id):
    ### TAREA: Complete la función a partir de aquí ###

    return render_template("show.html",hospital=hospital_id, patient= patient)


# Borra un paciente
@app.route('/hospitals/<hospital_id>/patients/<patient_id>/delete',methods=['GET','POST'])
def delete_patient(hospital_id,patient_id):
    ### TAREA: Complete la función a partir de aquí ###

    return redirect('/hospitals/'+hospital_id+'/patients?patientDeleted=true')


# Asigna un doctor y devuelve los datos del paciente
@app.route('/hospitals/<hospital_id>/patients/<patient_id>/assign_doctor/assigned', methods = ['POST','PUT'])
def assign_doctor(hospital_id,patient_id):
    ### TAREA: Complete la función a partir de aquí ###

    return render_template("show.html",hospital=hospital_id, patient= patient)

@app.route('/hospitals/<hospital_id>/patients/<patient_id>/assign_doctor',methods=['GET'])
def pass_doctor(hospital_id,patient_id):
    return render_template("assign_doctor.html",hospital=hospital_id, patient= patient_id)

# Muestras los medicos de un paciente
@app.route('/hospitals/<hospital_id>/patients/<patient_id>/show_doctors',methods=['GET','POST'])
def show_patient_doctors(hospital_id,patient_id):
    ### TAREA: Complete la función a partir de aquí ###

    return render_template("show_doctors.html",doctors=patient.doctors, patient= patient_id)

# Mostrar la información registrada para un hospital
@app.route('/hospitals/<hospital_id>/show',methods=['GET'])
def show_hospital(hospital_id):
    hospital = Hospital.objects.get(id=hospital_id)
    query = f'''
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT DISTINCT ?nombre
    # ¡ATENCIÓN!
    # Hay que utilizar doble corchete en estas consultas, porque es una f-string
            WHERE {{
                <{hospital.iri}> rdfs:label ?nombre .
            }}

    '''
    print(query)
    hospital_info = sparql(query)
    return render_template("show_hospital.html",
                           iri=hospital.iri,
                           hospital_info=hospital_info)

################### Espacio para seeders ############################

def seeder():
    print('#### Check Database seed ####')
    all_hospitals = Hospital.objects.all()

    if (len(all_hospitals) <= 0):
        print('#### Collections are empty ####')
        print('#### Adding some entries... ####')
        with open(os.path.join(os.path.dirname(__file__), 'seeders/seeders.json'), 'r', encoding='utf-8') as f:
            print('#### seeders.json file opened... ---####')
            data = json.load(f)

        for hospital in data['hospitals']:
            new_hospital = Hospital(**hospital)
            new_hospital.save()

        doctors = {}
        for doctor in data['doctors']:
            new_doctor = Doctor(id=doctor['id'], name=doctor['name'], surname=doctor['surname'], speciality=doctor['speciality'])
            new_doctor.save()
            doctors[doctor['id']] = new_doctor

        for patient in data['patients']:
            new_patient = Patient(id=patient['id'], name=patient['name'], surname=patient['surname'], dni=patient['dni'])
            hospital = Hospital.objects.get(id=patient['hospital_id'])
            new_patient.hospital = hospital
            if (patient['id'] == '3a268172-6c5c-4d9b-8964-8b9a1e531af5'):
                new_patient.doctors.append(doctors['014bd297-0a3d-4a17-b207-cff187690045'])
                new_patient.doctors.append(doctors['9bb2e300-fa15-4063-a291-13f7199ddb52'])
            elif (patient['id'] == '088d58e2-7691-47b6-a322-eeffcadc9054'):
                new_patient.doctors.append(doctors['a0f54d52-5ccb-4e50-adca-5ea0064262fd'])
            elif (patient['id'] == '8ec8c43b-f7e1-43e4-b70f-6d5a9799a86a'):
                new_patient.doctors.append(doctors['1497d1be-577a-41ad-b129-45271e113cc0'])
            elif (patient['id'] == '923ec756-87b7-4743-808b-795a04b6dd21'):
                new_patient.doctors.append(doctors['9bb2e300-fa15-4063-a291-13f7199ddb52'])
            new_patient.save()
        print('#### Finished! ####')
    else:
        print('#### Database already seeded ####')

seeder()
