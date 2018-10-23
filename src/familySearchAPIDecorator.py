import requests

class FSDecorator:
    """ A singleton decorator for the FamilySearch API"""
    # This code adapted from https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html


    class __FSDecorator:
        def __init__(self, session):
            self.session = session
        
        def postMemory(self, title, story_text, code_grant):
            pass
        
        def getMemory(self, id):
            url = "https://api-integ.familysearch.org/platform/memories/memories/"
            access_token = self.session['user']['accessToken']

            headers = {
                'Accept': "application/x-fs-v1+xml",
                'Authorization': "Bearer " + access_token,
                }

            response = requests.request("GET", url+id, headers=headers)

            return response

    instance = None
    def __init__(self, session):
        if not FSDecorator.instance:
            FSDecorator.instance = FSDecorator.__FSDecorator(session)
        else:
            FSDecorator.instance.session = session
    
    def getInstance(self):
        return FSDecorator.instance
