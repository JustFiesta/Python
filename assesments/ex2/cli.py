#!/usr/bin/env python

import argparse
import sys
import os
from dotenv import load_dotenv

import api_communication


class TooFewArgumentsException(Exception):
    """Exception for too few arguments passed"""
    def __init__(self, message):
        self.message = "Please specify required file parameters: survey mails"
        super().__init__(self.message)

"""
Custom parser subclass, throwing ArgumentParserError on too few arguments
"""
class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise TooFewArgumentsException(message)


# create cli parser with arguments
def create_parser():
    parser = ThrowingArgumentParser(description="""Post surveys on surveymonkey.com""")
    parser.add_argument("survey",
                        help="JSON file containing survey information")
    parser.add_argument("mails", 
                        help="TXT file containing participant mails")

    return parser


# run function
def main():

    # check if any arguments were passed - if not display help
    try:
        parser = create_parser()
        args = parser.parse_args()
    except TooFewArgumentsException:
        print("Please provided reqiured parameters!\n")

        parser.print_help()
        sys.exit(0)

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