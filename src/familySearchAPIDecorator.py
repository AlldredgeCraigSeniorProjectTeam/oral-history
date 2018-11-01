import requests
from xml.etree import ElementTree
from customExceptions import httpError401Exception, httpErrorUnhandledException

class FSDecorator:
    """ A singleton decorator for the FamilySearch API"""
    # This code adapted from https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html


    class __FSDecorator:
        def __init__(self, session):
            self.session = session
        
        def postMemory(self, title, story_text, code_grant):
            pass
        
        def getMemory(self):
            url = "https://api-integ.familysearch.org/platform/memories/memories/"
            access_token = self.session['user']['accessToken']

            headers = {
                'Accept': "application/x-fs-v1+xml",
                'Authorization': "Bearer " + access_token,
                }

            id = "751321"
            response = requests.request("GET", url+id, headers=headers)

            response_status_code = response.status_code
            print("The request returned a status code of " + str(response_status_code))


            if response.status_code == 200:
                root = ElementTree.fromstring(response.text)
                stories = root.findall(".//{http://gedcomx.org/v1/}description")

                speech_output = stories[0].text
                return speech_output
            elif response.status_code == 401:
                # You need to reauthenticate
                raise httpError401Exception()
            else:
                # Unhandled status code
                raise httpErrorUnhandledException(response_status_code)

    instance = None
    def __init__(self, session):
        if not FSDecorator.instance:
            FSDecorator.instance = FSDecorator.__FSDecorator(session)
        else:
            FSDecorator.instance.session = session
    
    def getInstance(self):
        return FSDecorator.instance
