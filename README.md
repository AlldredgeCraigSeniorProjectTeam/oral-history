![Project Logo](header.png)
###### Contributors: Jacob Alldredge and Daniel Craig

[![Build Status](https://travis-ci.com/AlldredgeCraigSeniorProjectTeam/oral-history.svg?branch=master)](https://travis-ci.com/AlldredgeCraigSeniorProjectTeam/oral-history)

### Summary
This is the senior project repo of Jake Alldredge and Daniel Craig. Our objective is to make an Amazon Alexa skill that interfaces with FamilySearch to collect and upload oral histories via Amazon Echo devices.

The oral-history will be the portion of our project that interacts with Alexa directly. User will dictate an oral history which Alexa
will then record and upload to FamilySearch.

# Our Stack
 - Node.js
 - Python
 - Amazon Echo Dot (2nd Gen)
 - Amazon Web Services (AWS)
   - AWS Lambda
   - Alexa and Amazon Lex
 - Family Search APIs
 - Travis CI

# Our Alexa skill's requirements
 - Be able to preserve dictated family stories
 - Be able to store preserved family stories on FamilySearch

# Our workflow
 - Contact Alexa
 - Creates Lex Conversation
   - lambda Looks for ancestor
     - Access FamilySearch w/ API
     - Record oral history
     - Return control to Lex
   - lambda Upload
     - Ask for confirmation
     - Access FamilySearch w/ API
     - Save to Memories
     - Return control to Lex
   - lambda Tell me a story about [ancestor]
     - Access FamilySearch w/ API
     - Access Memories
     - Read story
     - Return control to Lex

# Our team's definitions
| Term       | Definition |
|------------|------------|
| AWS   | Amazon Web Services  |
| IAM        | Identity and access management.  Where AWS permissions are managed.  |
| Intent     |            |
| Invoke     | The canonical term for starting the exection of a Lambda function    |
| Lambda     | A function that runs on AWS Lambda; no need for server config, etc.  |
| KMS   | Key Management Service  |
| Sample     |            |
| Slot       |            |
| SSML       |            |
