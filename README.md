# INTERACT (INTERnational survey on climate ACTion)

## Video Demo:  <https://youtu.be/9UQtcxF-Moo>

## Description

The INTERACT project (INTERnational survey on climate ACTion) aims to engage a people in a data - action exchange. By this we mean that the data will be used constructively to stimulate positive action.

The web application utilises several API's to return climate related data globally. It also makes use of the UNFCCC API to allow users (registered or unregistered) to query country emissions by GHG type. It then returns total emissions with and without Land Use Change, Land Use Change and Forestry.

The main purpose of this web application is the to allow users to register for an account, and to fill in a short online survey. All data is anonymous, data from the users are stored in an SQL database.
The user can view their submitted responses, however, only one survey submission per users is allowed.

The user can also view the results of all submissions on a global map, which summaries the inputs for the user.

Should the user wish to use the data, an API, along with documentation via the swagger UI, has been provided.

## INTERACT Conceptual Framework
<img src="https://drive.google.com/uc?id=1AUEieDb4-_-_j19OldRPHMJAn3Bl3G_r" width="600" height="400">

Ideally, we would like to collect data, and work towards expanding this project. Eventually, we would like the data collected via this web application to assist us in developing an action oriented tool kit that will increase participation in the general climate conversation, policy setting and research and development. It is very clear that key voices are either being drowned out, or not heard at all. And, time is running out to be heard.

## Basic Architechtural Overview
<img src="https://drive.google.com/uc?id=1p-UNg9zkDihOytbN5gX6Io9ZaKwFwrhU" width="600" height="400">

Outlined above is a basic overview of the application architechture. As can be seen, it relies on several 3rd party APIs to provide the climate data. The application uses Flask framework, with and SQL backend. The API for survey data is configured using swagger and interactive documentation is also provided.

## Project Contents
Below is a list of the various files included and their purpose.

### app.py
This is the main flask application and contains the various routes etc for the application.

### create_tables.sql
This file contains the SQL commands for setting up the various tables in the database. It will allow you to start with a clean database. However, be careful, running this with the db_table_create.py file will delete any existing tables and replace them with empty ones.

### db_table_create.py
This, as mentioned, is the companion file to create_tables.sql. This will create new tables, but erase existing ones.

### helpers.py
This file is essentially the API engine room. It also contains functions for password validation, and the "apology" function (utilised in pset9)

### survey_data.py
This file contains the read_all function specified in the swagger.yml file.

### swagger.yml
This is the API and API documentation configuration file.