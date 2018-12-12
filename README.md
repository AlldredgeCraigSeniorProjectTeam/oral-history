![Project Logo](header.png)
###### Contributors: Jacob Alldredge and Daniel Craig

[![Build Status](https://travis-ci.com/AlldredgeCraigSeniorProjectTeam/oral-history.svg?branch=master)](https://travis-ci.com/AlldredgeCraigSeniorProjectTeam/oral-history)

### Summary
This is the senior project repo of Jake Alldredge and Daniel Craig. Our objective is to make an Amazon Alexa skill that interfaces with FamilySearch to collect and upload oral histories via Amazon Echo devices.

# Our Stack
 - Python and Pip
 - Amazon Echo Dot 
 - Amazon Web Services (AWS)
   - AWS Lambda
   - Alexa 
 - Family Search APIs
 - Travis CI

# Our Alexa skill's requirements
 - Be able to preserve dictated family stories
 - Be able to store preserved family stories on FamilySearch

# Our workflow
 - Alexa interprets user input per the Dialog Model that we define.
 - Lambda backend handles intent requests using ASK SDK v.2.
   - Dependent on the intent recieved, Lambda will do one (or more) of the following:
     - Tell a story from FamilySearch, using the FamilySearch API and Alexa's text to speech abilities.
     - Record, transcribe, and upload a story to FamilySearch, using the API and Alexa's speech to text.
     - Interview the user, and upload the transcript to FamilySearch, using the API and Alexa's speech to text.

