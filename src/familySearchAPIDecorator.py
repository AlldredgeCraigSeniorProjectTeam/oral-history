import requests
import random
import json
from customExceptions import httpError401Exception, httpError403Exception, httpErrorUnhandledException, httpResponseCode204Exception


class FSDecorator:
    """ A singleton decorator for the FamilySearch API"""
    # Adapted from https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

    class __FSDecorator:
        def __init__(self, access_token):
            """ The constructor for the FSDecorator class takes one parameter, the access token, which
            it stores in its attributes """
            self.access_token = access_token

        def postMemory(self, story, title = "Story from Alexa"):
            """ This method posts a memory to FamilySearch"""
            url = "https://api-integ.familysearch.org/platform/memories/memories"

            querystring = {"title":title}

            payload = story
            headers = {
                'Content-Disposition': "attachment; filename='" + title + ".txt'",
                'Content-Type': "text/plain",
                'Authorization': "Bearer " + self.access_token,
                }

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

            if response.status_code == 201:
                speech_text = "Your memory was successfully added to Family Search!" 
                print speech_text
                return speech_text
            elif response.status_code == 401:
                # 401 error, reauthenticate
                raise httpError401Exception()
            elif response.status_code == 403:
                # 403 error, reauthenticate
                raise httpError403Exception()
            else:
                # Unhandled status code
                raise httpErrorUnhandledException(response.status_code)

        def getRandomMemoryID(self):
            """ This method randomly chooses the ID of one of the memories available on FamilySearch """
            url = "https://api-integ.familysearch.org/platform/memories/memories/"

            headers = {
                'Accept': "application/json",
                'Authorization': "Bearer " + self.access_token
                }

            response = requests.request("GET", url, headers=headers)
            print("The request returned a status code of " + str(response.status_code))

            if response.status_code == 200:
                responseData = json.loads(response.text)
                listOfMemories = responseData['sourceDescriptions']
                listOfMemoryIDs = [memory['id'] for memory in listOfMemories if memory['mediaType'] == 'text/plain']

                if len(listOfMemoryIDs) >= 1:
                    randomMemoryID = listOfMemoryIDs[random.randint(0, len(listOfMemoryIDs) - 1)]
                    return randomMemoryID
                else:
                    # Return a negative 1 if there are no text memories available
                    return -1
            elif response.status_code == 204:
                # There are no memories currently
                raise httpResponseCode204Exception()
            elif response.status_code == 401:
                # You need to reauthenticate
                raise httpError401Exception()
            elif response.status_code == 403:
                raise httpError403Exception()
            else:
                # Unhandled status code
                raise httpErrorUnhandledException(response.status_code)


        def getMemory(self):
            """ This method gets a memory from FamilySearch"""
            url = "https://api-integ.familysearch.org/platform/memories/memories/"

            headers = {
                'Accept': "application/json",
                'Authorization': "Bearer " + self.access_token,
                }

            # If this raises a 401 exception, we want it to bubble up to the calling function
            id = self.getRandomMemoryID()

            # getRandomMemory returns -1 if there are no memories available to listen to.
            if  id == -1:
                speech_output = "There are no memories available.  Please try recording a new memory so that you'll have something to listen to."
                return speech_output

            # We passed the -1 check, so assume that the id is good.
            response = requests.request("GET", url+id, headers=headers)

            response_status_code = response.status_code
            print("The request returned a status code of " + str(response_status_code))

            if response.status_code == 200:
                responseJsonObj = json.loads(response.text)
                urlOfMemoryText = responseJsonObj['sourceDescriptions'][0]['about']
            elif response.status_code == 204:
                # There are no memories currently
                raise httpResponseCode204Exception()
            elif response.status_code == 401:
                # You need to reauthenticate
                raise httpError401Exception()
            elif response.status_code == 403:
                raise httpError403Exception()
            else:
                # Unhandled status code
                raise httpErrorUnhandledException(response_status_code)

            memoryTextResponse = requests.request("GET", urlOfMemoryText, headers=headers)
            memoryText = memoryTextResponse.text
            return memoryText

    instance = None
    def __init__(self, access_token):
        """ The constructor of the FSDecorator class, it creates an instance of the hidden class if
        need be ."""
        if not FSDecorator.instance:
            FSDecorator.instance = FSDecorator.__FSDecorator(access_token)
        else:
            FSDecorator.instance.access_token = access_token

    def getInstance(self):
        """ Get the single instance of the Singleton Class """
        return FSDecorator.instance
