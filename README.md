# compeition-registration-service
This project is the backend system for a competition registration system. It allows administrators to create a competition in a database, and then allows users to create accounts and register themselves for competitions.

## Architecture Overview (TODO: Write)
High-level description of your services and their interactions.
More detail can be found in ./SYSTEM_ARCHITECTURE.md

## Prerequisites (TODO: Add versions and ensure everything here to run container)
Required software:
- Docker
- Docker Compose

## Installation & Setup (TODO: Write)
Step-by-step instructions to get the system running

## Usage Instructions (TODO: Write)
How to check health of your services (example curl commands or API endpoints)

## API Documentation (TODO: Write)
List of all health endpoints with request/response examples

## Testing (TODO: Write)
How to test the system (manual testing steps or test commands)

## Project Structure
competition-registration-system/\
├── .gitignore\
├── README.md\
├── CODE_PROVENANCE.md\
├── SYSTEM_ARCHITECTURE.md\
├── architecture-diagram.png\
├── docker-compose.yml\
├── admin-service/\
│&emsp;&ensp;├── Dockerfile\
│&emsp;&ensp;├── requirements.txt\
│&emsp;&ensp;├── main.py\
│&emsp;&ensp;└── models.py\
└── user-service/\
&emsp;&emsp; ├── Dockerfile\
&emsp;&emsp; ├── requirements.txt\
&emsp;&emsp; ├── main.py\
&emsp;&emsp; └── models.py
