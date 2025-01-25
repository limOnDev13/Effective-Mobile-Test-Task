# JavaCode test task
A test assignment from the JavaCode company.

## Description
A full-featured Django web application for managing cafe orders. The application allows you to add, delete, search, edit and display orders.

## Demo

![](demo.gif)

---
## Setup and launch

To launch the application, it is enough to download the project to the machine (you don't have to download the files in the tests, files requirements-dev.txt , setup.cfg), set environment variables as shown in the example .env.example and assemble docker containers (using the ```docker compose up --build``` command from the project root). 

If the application is running on a local machine, requests can be sent to http://127.0.0.1:8080.
___

## Main refs
**/orders/** - List of orders
By going to this address, it will become clear how the web interface works.

## Endpoints

The application has its own API.

- **GET /orders/api/** - Get list of orders
- **POST /orders/api/** - Create a new order
- **GET /orders/api/<int:pk>/** -Get the order
- **PUT and PATCH /orders/api/<int:pk>/** - Update the order
- **DELETE /orders/api/<int:pk>/** - Delete the order

For more detailed documentation, you can use Swagger (http://127.0.0.1:8080/api/docs )
___

## Technologies
- Django
- DRF 
- Postgres
- Docker
- Nginx
- Swagger
- unittest
