# Hosptial Management REST Api

The goal of the project is to implement an API that can manage information from a hospital according to 3 roles "General Manager", "Doctor" and "Assistant".

## Description

The project is created with the help of the Flask framework along with some of its specific dependencies.

## Getting Started
To test the REST Api we can use different methods. My recommendation is Postman.

1. Clone this repository: git clone https://github.com/PurceaIonut/hospital-management.git <br />
2. Navigate to the project directory: cd <repository-name> <br />
3. Install the required dependencies: pip install -r requirements.txt <br />


### Dependencies

* Flask
* Flask-JWT-Extended
* Flask-SQLAlchemy
* Flask-JWT-Extended


## Endpoints
### Register Route
admin = User(email= 'general_manager@example.com', password = 'password', role= 'General Manager'), we can change email and password from our app.py <br />
<br />
GET /register/admin

### Login Route
POST /login <br />

``` json
{
  "email": "general_manager@example.com",
  "password": "password"
}
```

### Doctors
POST /doctor (requires authentication) - creates a new doctor <br />
GET /doctors (requires authentication) - retrieves all doctors <br />
DELETE /doctor/<id> (requires authentication) - deletes a doctor by ID <br />
### Patients<br />
POST /patient (requires authentication) - creates a new patient <br />
GET /patients (requires authentication) - retrieves all patients <br />
DELETE /patient/<id> (requires authentication) - deletes a patient by ID <br />
### Assistants <br />
POST /assistant (requires authentication) - creates a new assistant <br />
GET /assistants (requires authentication) - retrieves all assistants <br />
DELETE /assistant/<id> (requires authentication) - deletes an assistant by ID <br />
### Authentication <br />
This API uses JSON Web Tokens (JWT) for authentication. To access any of the endpoints that require authentication, you must include a valid JWT token in the Authorization header of your HTTP request.
<br />

### Doctor Treatment
POST /treatment/patient/assign

Assigns a treatment to a patient by a doctor.

Request body:
 
``` json
{
  "name": "Treatment name",
  "description": "Description of treatment",
  "patient_id": 123,
  "doctor_id": 456
}
```
### Assign Patient
POST /patient/{patient_name}/assign

Assigns a patient to an assistant.

Request body:

``` json
{
   "assistant_id": 789
}
```

### Assistant Treatment
POST /treatment/patient/assign

Assigns a treatment to a patient by an assistant.

Request body:

``` json
{
  "name": "Treatment name",
  "description": "Description of treatment",
  "patient_id": 123,
  "assistant_id": 789
}
```

### Report Doctors

GET /report

Returns a report containing the list of all the doctors and the associated patients.

Response body:

``` json
{
  "report": [
    {
      "doctor": "Doctor name",
      "patients": [
        {
          "id": 123,
          "name": "Patient name",
          "email": "patient@email.com"
        },
      ]
    },
  ],
  "statistics": {
    "total_doctors": 5,
    "total_patients": 20,
    "total_treatments": 30
  }
}
```

### Get Patient Treatments
GET /patient/{patient_name}/treatments

Returns a report with all the treatments applied to a patient (JSON).

Response body:
``` json
{
  "name": "Treatment name",    
  "description": "Description of treatment"
}
```
## Vulnerabilities
1. Passwords are stored as plain text in the database, which makes them vulnerable to attacks if the database is compromised. <br />
2. The access token is not being verified for each request. <br />
3. There is no session timeout or logout mechanism, which could allow an attacker to hijack an authenticated session if they gain access to the user's access token.


## Authors

Purcea Ionut Mihai

## Version History

* 0.1
    * Initial Release


