# System Architecture

## System Purpose
This system provides a database organization for compeitions. It allows administrators to create competitions in the database. Users are then able to make an account and register their account to previously created competitions.

## Service Boundaries
The admin-service is responsible for the oversight and management of the competitions themselves. Admins are able to create competitons, view the people registered to them, add registrations, and remove registrations.

The user-service is responsible for allowing users to define their information and self register or remove themselves from competitions. This service can also view the list of competitions but cannot edit any entries aside from their own.

These services are separated in order to ensure that the people running the competitions have full access to records, without allowing competitors the same oversight. This way any managerial duties can be carried out by only authorized users.

## Data Flow
Both the user and admin services will rely on the health of each other in order for the system to function entirely. While some functions such as creation of new competitions or users can be done with no crossover, other functions such as viewing and editing registrations or self registration will require access to the other service.

Due to this, health checks at both services must ensure the services themselves are up at the bare minimum. Beyond that, health checks should include reaching to the other service as well as the redis database to ensure all functionality would be available.

This means when either service receives a full health check, it will also pull data from the other service's health check, as well as pinging redis.

## Communication Patterns
In order to obtain the health check from the other service, httpx will be used. This will request the other services base health check to ensure it is up and running.

The other communication will occur through a redis client instantiated at both services. This will send a ping command using the redis python library.

## Technology Stack
- Docker
    - Ensures each service runs with the proper dependencies, standardizes runtime, and organizes the system into individual containers.
- Docker Compose
    - Organizes services, networks, volumes, and dependencies properly.
- httpx
    - Allows communication between services in order to cross check health
- redis
    - Allows for a quick and easily health-checkable database to be integrated.
- Pydantic
    - Allows for easy verification of data going in and out of the system.
