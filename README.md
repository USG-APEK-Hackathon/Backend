# Hackathon-Backend

[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Hackathon project backend development. Check out the project's [documentation](https://github.com/USG-APEK-Hackathon/Backend).


## Table of contents


* [Stack](#stack)
* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Endpoints](#endpoints)

## Stack

* Framework: Django + Django REST Framework
* Formatters: Black
* Documentation: Drf-spectacular
* Containerization: Docker

## Prerequisites

This project can be run through Docker and local machine. For running through Docker, all you need is Docker. Otherwise, your machine needs to have Python (v 3.10), and PostgreSQL(v 14.5) installed.

## Setup

Description of how to set up the project to be able to start the development.


### If using docker

Before running these, make sure you have created `.env` files in dirs where `.env.example` is present and include all required variables there.

    # Build the project.
    $ docker-compose -f docker/local/docker-compose.yml build

    # Start the project.
    $ docker-compose -f docker/local/docker-compose.yml up -d

    # Stop the project.
    $ docker-compose -f docker/local/docker-compose.yml down

### If running without docker

Before running these make sure to create `.env` file in base directory with all required variables. See `.env.example` file

    # Install dependencies.
    $ pip install -r requirements.txt

    # Start the project.
    $ make run

you also need to make sure that postgres is installed and running on your machine

## Endpoints

Endpoints can be viewed at swagger and redoc. They will be available after project has been successfully set up and running.

* Swagger: /api/schema/swagger-ui/
* Redoc: /api/schema/redoc/
