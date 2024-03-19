CLI survey poster 
-----------------

This folder contains simple script connecting to SurveyMonkey API, via API token stored in .env file 

Using simple CLI, it takes two values like: <survey.json> <emails.txt>, and then sends survey to surveymonkey API, also sanding the invitations to end users specified in email.

Usage
-----

`python3 .\cli.py .\survey.json .\emails.txt`

NOTE: remember to pass API_TOKEN to `.env` file in same directory as `cli.py`


