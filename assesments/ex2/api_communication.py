import http.client # import http library
import json

# endpoint = https://api.surveymonkey.com/v3
# surveys folder = https://api.surveymonkey.com/v3/surveys
# survey collector invitation = https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors

"""
Global variables needed for each funciton
"""
surveys_url =  '/v3/surveys'
survey_id = ""


"""
Creates and returns connection to api.surveymonkey.com
"""
def craete_connection():
    conn = http.client.HTTPSConnection("api.surveymonkey.com")
    return conn


"""
Custom exceptions
"""
class APIConnectionException(Exception):
    """"Universal exception raised for any API errors.
    
    Attributes:
    method -- method with caused the error (eg. POST, GET, etc.)
    target -- survey monkey target (eg. survey, collector, invites, etc.)
    response_status -- response status code
    response_data -- whole response - explanation of the error
    """

    def __init__(self, method, target, response_status, response_data):
        self.method = method
        self.target = target
        self.response_status = response_status
        self.response_data = response_data
        self.message = f"Failed to {method} {target}: {response_status}\nWhole response data: {response_data}"
        super().__init__(self.message)


"""
Post survey from json file
"""
def post_survey(api_token, survey_json_file):

    # setup http connection client
    conn = craete_connection()

    # read file contents
    with open(survey_json_file, 'rb') as survey_file:
        survey_data = json.load(survey_file) # make an python obj from file contents
    
    survey_json_string = json.dumps(survey_data) # convert json dictonary to string

    # headers for http POST requests with API for authorisation
    headers_POST = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {api_token}"
    }
    
    # send survey json string
    conn.request("POST", surveys_url, survey_json_string, headers_POST)
    response = conn.getresponse()
    data = response.read() # check whole response msg

    if response.status == 201:
        print("Survey posted!!!")
    else:
        raise APIConnectionException("POST", "survey", response.status, data)


"""
Get last survey id
"""
def get_survey_id(api_token):

    # prepare connection
    conn = craete_connection()
    
    # headers for GET request
    headers_GET = {
        'Accept': "application/json",
        'Authorization': f'Bearer {api_token}'
    }

    # get survey list
    survey_list = conn.request("GET", surveys_url, headers=headers_GET)
    response = conn.getresponse()
    data = response.read() # check whole response msg

    if response.status == 200:
        print("Got survey list!!!")
    else:
        raise APIConnectionException("GET", "survey list", response.status, data)
    
    # return last createad survey id
    return survey_list[-1]


"""
Create collector and send survey invitations through it
"""
def post_survey_invitations(api_token, survey_id, email_list_file):

    # prepare connection
    conn = craete_connection()

    # headers for http requests with API for authorisation
    headers_POST = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    # API endpoint link for certain survey
    invitations_url = f'surveys/{survey_id}/collectors'

    # create new collector for invitations
    collector_data = {
        "type": "email",
        "name": "Work satisfaction",
        "display_survey_results": True,
        "anonymous_type": "fully_anonymous",
        "sender_email": "mbocak@griddynamics.com",
        "width": 400,
        "height": 500,
        "border_color": "#FF4880",
        "is_branding_enabled": True,
        "respondent_authentication": False,
        }

    # create collector
    conn.request("POST", invitations_url, json.dumps(collector_data).encode('utf-8'), headers_POST)
    response = conn.getresponse()
    data = response.read()

    if response.status == 200:
        # get collector id from server response
        collector_id = response.json()["id"]
        print("Collector created successfully!")
    else:
        raise APIConnectionException("POST", "collector", response.status, data)


    # read email list for invites
    with open(email_list_file, 'r') as email_file:
        email_list = email_file.readlines()

    # for each email create new invitation
    for email in email_list:
        invitation_data = {
            "type": "email",
            "collector_id": collector_id,
            "send": True,
            "recipients": {
                "email": email.strip()
            }
        }
    
    # send invitations
    conn.request("POST", invitations_url + f'/{collector_id}/messages', json.dumps(invitation_data), headers_POST)
    
    # check response status
    if response.status == 200:
        print(f"Invitation sent successfully to {email.strip()}")
    else:
        raise APIConnectionException("POST", "invitations", response.status, data)
