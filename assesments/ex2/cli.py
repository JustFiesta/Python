#!/usr/bin/env python

import argparse
import sys
import os
from dotenv import load_dotenv

import api_communication

# create cli parser with arguments
def create_parser():
    parser = argparse.ArgumentParser(description="""Post surveys on surveymonkey.com""")
    parser.add_argument("survey",
                        help="JSON file containing survey information")
    parser.add_argument("mails", 
                        help="TXT file containing participant mails")

    return parser

# run function
def main():

    try:
        parser = create_parser()
    except TypeError:
        print("JSON survey file and email list file ARE REQUIRED!")
        create_parser().print_help()
    
    args = parser.parse_args()

    # check if any arguments were passed - if not display help
    if all(value is None for value in vars(args).values()):
        parser.print_help()
        sys.exit(0)
    else:
        # api token from evnrioment variable
        try:
            load_dotenv()
            api_token = os.environ['SURVEY_MONKEY_API']
        except KeyError:
            print("Please first set enviroment variable with API token to survey monkey")
            sys.exit(1)

        # both are required by parser (as positionals on default), so no need to exit if they are not present
        if args.survey:
            survey_json_file = str(args.survey)
        if args.mails:
            email_list_file = str(args.mails)

        # try to send survey and if succeded send invitations
        try:
            api_communication.post_survey(api_token, survey_json_file)
        except ConnectionError:
            print("API connection error - survey not posted!")
            sys.exit(1)
        
        try:
            api_communication.post_survey_invitations(api_token, api_communication.survey_id, email_list_file)
        except ConnectionError:
            print("API connection error - emails not sent!")
            sys.exit(1)


# run main if main module is in use
if __name__ == '__main__':
    main() 