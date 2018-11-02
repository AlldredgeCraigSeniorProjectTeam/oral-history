# test.py

import requests
import json

url = "https://api-integ.familysearch.org/platform/memories/memories/754816"

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer e5bed874-a37e-4046-af0e-57809ba9a133-aws-integ",
    'cache-control': "no-cache",
    'Postman-Token': "c0969a95-6a06-4767-bf73-3d022900c8b2"
    }

response = requests.request("GET", url, headers=headers)

responseData = json.loads(response.text)
memoryURL = responseData['sourceDescriptions'][0]['about']

completeStoryResponse = requests.request("GET", memoryURL, headers=headers)
story = completeStoryResponse.text

print(story)
