#!/usr/bin/env python

import requests # import http library
import json

# endpoint = https://api.surveymonkey.com/v3
# surveys folder = https://api.surveymonkey.com/v3/surveys
# survey collector invitation = https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors

survey_id = ""

def post_survey(api_token, survey_json_file):
    # read file contents
    with open(survey_json_file, 'r') as survey_file:
        survey_data = survey_file.read()

    # headers for http requests with API for authorisation
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    # send survey json
    survey_url =  'https://api.surveymonkey.com/v3/surveys'
    response = requests.post(survey_url, headers=headers, data=survey_data)

    if response.status_code == 200:
        #survey_id = response.json()[id]
        print("Survey posted!!!")
    else:
        print("Failed to post survey. Status code: ", response.status_code)
    

def send_survey_invitations(api_token, survey_id, email_list_file):

    # headers for http requests with API for authorisation
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    # API endpoint link for certain survey
    invitations_url = f'https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors'

    # create new collector for invitations
    collector_data = {
        "type": "email",
        "name": "Email Collector"
    }

    # send survey json
    response = requests.post(invitations_url, headers=headers, data=json.dumps(collector_data))

    if response.status_code == 200:
        # get collector id from server response
        collector_id = response.json()[id]
        print("Survey sent successfully!")
    else:
        print("Failed to send survey. Status code:", response.status_code)

    # read email list for invites
    with open(email_list_file, 'r') as email_file:
        email_data = email_file.read()

    # for each email create new invitation
    for email in email_file:
        invitation_data = {
            "type": "email",
            "collector_id": collector_id,
            "send": True,
            "recipients": {
                "email": email.strip()
            }
        }
    
    # send invitations
    response = requests.post(invitations_url + f'/{collector_id}/messages', headers=headers, data=json.dumps(invitation_data))
    
    # check response status
    if response.status_code == 200:
        print(f"Invitation sent successfully to {email.strip()}")
    else:
        print(f"Failed to send invitation to {email.strip()}. Status code:", response.status_code)


def main():
    api_token = 'TOKEN_STR'
    survey_json_file = 'survey.json'
    email_list_file = 'emails.txt'

    post_survey(api_token, survey_json_file)

    survey_id = 'ID'

    send_survey_invitations(api_token, survey_id, email_list_file)


# run main if main module is in use
if __name__ == '__main__':
    main() 