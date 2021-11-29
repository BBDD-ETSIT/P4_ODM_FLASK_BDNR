<img  align="left" width="150" style="float: left;" src="https://www.upm.es/sfs/Rectorado/Gabinete%20del%20Rector/Logos/UPM/CEI/LOGOTIPO%20leyenda%20color%20JPG%20p.png">
<img  align="right" width="60" style="float: right;" src="http://www.dit.upm.es/figures/logos/ditupm-big.gif">


<br/><br/>


# Practica BDNR - FLASK ODM - MONGOENGINE

## 1. Objetivo

- Desarrollar las 4 operaciones CRUD (Create, Read, Update and Delete) a través de un ODM
- Practicar con un ODM para realizar queries
- Afianzar las ventajas de usar ODMs en el desarrollo de aplicaciones
- Realizar consultas semánticas usando SPARQL

## 2. Dependencias

Para realizar la práctica el alumno deberá tener instalado en su ordenador:
- Entorno de ejecución de Python 3 [Python](https://www.python.org/downloads/)
- Base de datos MongoDB [MongoDB](https://www.mongodb.com/try/download/community)
- Base de datos [Fuseki](https://jena.apache.org/documentation/fuseki2/)

## 3. Descripción de la práctica

La práctica simula una aplicación de gestión de pacientes basada en el patron MVC (Modelo-Vista-Controlador) utlizando la librería Flask de python. La práctica tambien usa MongoEngine como ODM para poder almacenar los datos de la aplicación en MongoDB, y conexiones a un endpoint SPARQL mediante `SPARQLWrapper`.

La **vista** es una interfaz web basada en HTML y CSS que permite realizar diversas acciones sobre los pacientes como crear, editar, buscar, filtrar, listar o eliminar. La vista esta incluida ya en el codigo descargado.

El **modelo** es la representación de la información de los pacientes. En esta aplicación se van a usar tres modelos: doctor, hospital y patient. Un ejemplo de como están definidos los modelos en esta práctica es el siguiente (la definición de todos los modelos se encuentra en `models.py`):

```
class Patient(db.Document):
    id = db.StringField(primary_key=True, required=True)
    name = db.StringField(required=True)
    surname = db.StringField(required=True)
    dni = db.StringField(required=True)
    hospital = db.ReferenceField(Hospital)
    doctors = db.ListField(db.ReferenceField("Doctor")) 
```

El **controlador** ejecuta acciones sobre los modelos. El alumno deberá desarrollar varias funciones del controlador para que las acciones que se realicen a través de la página web funcionen correctamente. Para ello, desarrollara las operaciones correspondientes con MongoEngine implementando las operaciones CRUD sobre los objetos patiente, hospital y doctor, así como otra serie de queries.

En el siguiente video puede observar cuál sería el funcionamiento normal de la aplicación [link](https://youtu.be/8xXaFCRxMXE)

## 4. Descargar e instalar el código del proyecto

Abra un terminal en su ordenador y siga los siguientes pasos.

Descárguese y descomprima el código pinchando más arriba en el botón code y eligiendo opción "Download ZIP".

Navegue a través de un terminal a la carpeta P4_ODM_FLASK_BDNR.
```
> cd P4_ODM_FLASK_BDNR
```

Una vez dentro de la carpeta, se instalan las dependencias. Para ello debe crear un virtual environment de la siguiente manera:

```
[LINUX/MAC] > python3 -m venv venv
[WINDOWS] > py.exe -m venv env
```

Si no tiene instalado venv, Lo puede instalar de la siguiente manera:

```
[LINUX/MAC] > python3 -m pip install --user virtualenv
[WINDOWS] > py.exe -m pip install --user virtualenv
```

Una vez creado el virtual environment lo activamos para poder instalar las dependencias:

```
[LINUX/MAC] > source venv/bin/activate
[WINDOWS] > .\env\Scripts\activate
```

Instalamos las dependencias con pip:

```
> pip3 install -r flaskr/requirements.txt 
```

Indicamos a Flask el fichero con el que arrancar el servidor:

```
[LINUX/MAC] >  export FLASK_APP=flaskr/run.py
[WINDOWS] > $env:FLASK_APP = "flaskr/run.py"
```
Debemos tener arrancado MongoDB. Dependiendo de cómo lo hayamos instalado arrancará solo al iniciar la máquina o tendremos que ir a ejecutar el programa "mongod" a la carpeta bin donde hayamos realizado la instalación.

Podemos arrancar el servidor con el siguiente comando. Hasta que no realize el primer ejercicio sobre la configuración de la URI, el servidor no arrancara.

```
$ flask run
```


Abra un navegador y vaya a la url "http://localhost:5000" para ver la aplicación de gestión de pacientes.

**NOTA: Cada vez que se quiera realizar una prueba del código desarrollado, debemos parar y arrancar de nuevo la practica. Para ello, desde el terminal pulse ctrl+c para parar y arranque de nuevo con npm start**

**NOTA2: Si ha modificado alguna tabla de manera indeseada y se quiere volver a restablecer los valores por defecto, borre la base de datos odm_bddd y vuelva a arrancar el servidor con flask.**

## 5. Tareas a realizar


El alumno deberá editar el fichero `flaksr.run.py`.

Primero, deberá definir la URI de Conexión a la base de datos con nombre **odm_bbdd** :

```
app.config['MONGODB_SETTINGS'] = {### Definir la URI de la BBDD}
```

Después, se le provee un esqueleto con todas los funciones que deberá rellenar.
En cada una de estas funciones se deberá hacer uso del ODM MongoEngine o de SPARQL para realizar operaciones con la base de datos y devolver un resultado de la operación.


Las funciones son las siguientes:

### show_hospitals()

**Descripción:**
- Busca en la base de datos todos los hospitales existentes en la coleccion "Hospital"

**Parametros:**

- Ninguno

**Returns:**

- Un array de objetos de hospitales

### filterHospitalsByCity()

**Descripción:**
- Busca en la colección "Hospital" filtrando por ciudad
- Para acceder a la ciudad debe usar :
```
city = request.form['city']
```
**Parametros:**

- Ninguno

**Returns:**

- Un array de objetos de hospitales

### list_hospital_patients(hospital_id)

**Descripción:**
- Busca todos los pacientes correspondientes a un hospital ordenados por el nombre (de la A a la Z)

**Parametros:**

- hospital_id - Id del hospital

**Returns:**

- Un array de objetos de pacientes

### read_patient(hospital_id, patient_id)

**Descripción:**
- Busca los datos de un paciente

**Parametros:**

- hospital_id - Id del hospital
- patient_id - Id del paciente a actualizar

**Returns:**

- Un objeto paciente

### create_patient(hospital_id)

**Descripción:**
- Crea un paciente dentro de un hospital

**Parametros:**


- id - id del Paciente, debe generarse con:
```
id = uuid.uuid4()
```
- name - Nombre del paciente
- surname - Apellido del paciente 
- dni - DNI del paciente
- hospital_id - Id del hospital

**Returns:**

- El objeto paciente creado

### update_patient(hospital_id, patient_id)

**Descripción:**
- Actualiza los datos del paciente identificado por patient_id

**Parametros:**

- hospital_id - Id del hospital
- patient_id - Id del paciente
- name - Nombre del paciente
- surname - Apellido del paciente 
- dni - DNI del paciente

**Returns:**

- El objeto paciente actualizado

### delete_patient(patient_id)

**Descripción:**
- Borra un paciente de la base de datos

**Parametros:**

- patient_id - Id del paciente

**Returns:**

- El resultado de la operación de borrado

### assignDoctor(hospital_id, patient_id)

**Descripción:**
- Asigna un medico a un paciente en la base de datos.
- Para acceder al id del doctor puede usar:
```
doctor_id = request.form['doctor']
```
**Parametros:**

- patient_id - Id del paciente
- hospital_id - Id del hospital

**Returns:**

- Devuelve los datos del paciente al que se le ha asignado el medico

### show_patient_doctors(hospital_id, patient_id)

**Descripción:**
- Devuelve los doctores que estan asignados a un paciente.

**Parametros:**

- patient_id - Id del paciente
- hospital_id - Id del hospital

**Returns:**

- Un array de objetos de doctores 

### show_hospital(hospital_id)

Esta función será la encargada de mostrar información sobre un hospital en particular.
A diferencia del resto de apartados, en este caso la información se conseguirá de una fuente semántica: DBpedia.

Para ello, primero deberá recuperar el hospital (usando el ODM), para de esa forma acceder a su IRI.
Mediante la función `sparql` (importada de `models`), debe realizar una consulta SPARQL a DBpedia, conteniendo al menos 6 elementos de información sobre el hospital. p.e., dirección de contacto, número de camas en el hospital, año de apertura, etc.

Se proporciona una consulta de prueba en la que se muestra el nombre (etiqueta) del hospital, y que deberá modificar.

## 7. Instrucciones para la Entrega y Evaluación.

El alumno deberá subir a Moodle únicamente el fichero *run.py* con las modificaciones realizadas. 

**RÚBRICA**: Cada método que se pide resolver de la practica se puntuara de la siguiente manera:
-  **0.5 puntos por cada uno de las siguientes funciones realizadas:**  `list_hospitals`, `filterHospitalsByCity`, `list_hospital_patients`, `read`, `showPatientDoctors` y `delete`.
-  **1.5 puntos por cada uno de las siguientes funciones realizadas:**  `assignDoctor`, `create_patient` y `update_patient`
- **2.5 puntos** por la función `show_hospital`.
