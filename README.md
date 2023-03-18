# Hosptial Management REST Api

The goal of the project is to implement an API that can manage information from a hospital according to 3 roles "General Manager", "Doctor" and "Assistant".

## Description

The project is created with the help of the Flask framework along with some of its specific dependencies.

## Getting Started
To test the REST Api we can use different methods. My recommendation is Postman.

1. Install Postman, create new collection, add HTTP request.
2. In our file we have a route /register/admin, we can modify this according to the email and password we want to use for Login, with this we can further create other users depending on the role
3. To create General Manager account in our database we use http://localhost:5000/register/admin with method 'GET' 


### Dependencies

* Flask
* Flask-JWT-Extended
* Flask-SQLAlchemy


## Executing program
After taking the steps from Getting Started

1. In our Postman select Body -> Raw ->Json. Connect to account with {"email" : "insert General Manager email", "password": "insert password"
2. Login with our General Manager with http://localhost:5000/login ('POST' method).we will get an "access_token" which we put in the tab Authorization -> Type: Bearer Token -> Token. Now we are connected with the general manager role, we can use the following requests:<br />
-Doctor Management (Create new Doctor account, list all doctors, delete a doctor) <br />
-Patient management (Create new Patient account, list all patients, delete a patient, Patient assignment to a Assistant) <br />
-Assistant Management (Create new Assistant account, list all assistants, delete an assistant).<br /> 
-A report containing the list of all the Doctors and the associated patients and a
section for statistics data (JSON). <br />
-A report with all the treatments applied to a Patient (JSON)<br />

3. If we want to create a doctor/patient/assistant, we will do it in the following way: <br />
-http://localhost:5000/doctor with body : {"email" : "insert doctor email", "name" : "insert doctor name", "password": "insert doctor password"}, only General Manager account can create a new Doctor (method='POST') <br />
-http://localhost:5000/patient with body : {"email" : "insert patient email", "name" : "insert patient name", "password": "insert patient password"}Doctor and General Manager can create a new Patient(method='POST')<br />
-http://localhost:5000/assistant with body : {"email" : "insert assistant email", "name" : "insert assistant name", "password": "insert assistant password"}only General Manager account can create new Assistant (method='POST') <br />

4.If we want to access a report containing the list of all the Doctors and the associated patients and a
section for statistics we can with 



## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Purcea Ionut Mihai

## Version History

* 0.1
    * Initial Release


