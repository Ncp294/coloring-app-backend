# System Architecture

## System Purpose
This system provides a backend for a coloring application. It allows users to register and create their own custom templates to color on in the application. The template service converts user submitted images into coloring templates and returns them to the user. It also manages a public template database in case users wish to share their templates.

## Service Boundaries
The template-service is responsible for the oversight and management of the templates. This service will create templates from images, send templates to user profiles, and add or remove templates from the public database.

The user-service is responsible for allowing users to define their information to register for the application. They are also able to upload images to become templates, as well as access the public database and their own personal database of templates.

These services are separated in order to ensure that the users can only access templates allowed to them, as not all users would wish to share their own. Additionally, it will help easily enforce moderation over the public database by separating it into its own admin-like serivce.

## Data Flow
The user-service will rely on the template-service to complete some of its function, but the template service can stand alone.

Due to this, health checks at the template-service can simply focus on itself and the public database, while the user-service checks will reach out to the template-service in addition to itself and the user specific database.

## Communication Patterns
In order to obtain the health check from the template-service, the user-service will use httpx to send a request to that health check.

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
