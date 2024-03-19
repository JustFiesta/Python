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

    parser = create_parser()
    args = parser.parse_args()

    # check if any arguments were passed - if not display help
    if all(value is None for value in vars(args).values()):
        parser.print_help()
        sys.exit(0)
    else:

        # both are required by parser (as positionals on default), so no need to exit if they are not present
        if args.survey:
            survey_json_file = str(args.survey)
        if args.mails:
            email_list_file = str(args.mails)

        try:
             # try to load api token from evnrioment variable
            load_dotenv()
            api_token = os.environ['SURVEY_MONKEY_API']

            api_communication.post_survey(api_token, survey_json_file)
            api_communication.post_survey_invitations(api_token, api_communication.survey_id, email_list_file)
        
        except api_communication.APIConnectionException as e:
            print(e)
            sys.exit(1)


# run main if main module is in use
if __name__ == '__main__':
    main() 