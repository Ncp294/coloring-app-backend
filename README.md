# coloring-app-backend
This project is the backend system for a coloring app. This app includes the function of converting your own images into custom templates and allowing them to be shared amongst other users.

## Architecture Overview
The user service is able to register for the app, create custom templates, and store their works. The template service processes user images into templates and manages the public template database if users wish to share their templates.

The user service sends images to the template service and receives templates in return.

More detail can be found in ./SYSTEM_ARCHITECTURE.md

## Prerequisites
Required software:
- Python
- Docker
- Docker Compose
- (Other dependencies should be downloaded when the project is built)

## Installation & Setup
In the root folder of the directory, enter the command: 'Docker compose up --build -d'

That will build all the services in the system and get everything running on your local machine.

## Usage Instructions
Once the system is running, enter the following URLs in a browser to check the health of the services:

User service: http://localhost:8080/users/health

Template service: http://localhost:8080/template/health

## API Documentation
User Service:
- /users/health - Checks the health of the user service
    - Example:
        - Request: http://localhost:8080/users/health
        - Response: {"service":"user-service","status":"healthy","dependencies":[{"service":"redis","status":"healthy","response_time_ms":0},{"service":"template-service","status":"healthy","response_time_ms":28}]}

Template Service:
- /template/health - Checks the health of the template service
    - Example:
        - Request: http://localhose:8080/template/health
        - Response: {"service":"template-service","status":"healthy","dependencies":[{"service":"redis","status":"healthy","response_time_ms":0}]}

## Testing
To test the current system:
- Run the command: 'Docker compose ps'
    - Ensure all listed containers have a healthy status
- Access the health checks for both the user and template services
    - Ensure these return a healthy status for the main services and their dependencies

## Project Structure
competition-registration-system/\
├── .gitignore\
├── README.md\
├── CODE_PROVENANCE.md\
├── SYSTEM_ARCHITECTURE.md\
├── ARCHITECTURE_DIAGRAM.png\
├── docker-compose.yml\
├── nginx/\
│&emsp;&ensp;└── nginx.config\
├── template-service/\
│&emsp;&ensp;├── app/\
│&emsp;&ensp;│&emsp;&ensp;├── main.py\
│&emsp;&ensp;│&emsp;&ensp;└── models.py\
│&emsp;&ensp;├── Dockerfile\
│&emsp;&ensp;└── requirements.txt\
└── user-service/\
&emsp;&emsp; ├── app/\
&emsp;&emsp;&ensp;│&emsp;&ensp;├── main.py\
&emsp;&emsp;&ensp;│&emsp;&ensp;└── models.py\
&emsp;&emsp; ├── Dockerfile\
&emsp;&emsp; └── requirements.txt
