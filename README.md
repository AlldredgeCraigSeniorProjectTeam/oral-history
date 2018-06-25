![Project Logo](header.png)
###### Contributors: Jacob Alldredge and Daniel Craig

[![Build Status](https://travis-ci.com/AlldredgeCraigSeniorProjectTeam/oral-history.svg?branch=master)](https://travis-ci.com/AlldredgeCraigSeniorProjectTeam/oral-history)

### Summary
This is the senior project repo of Jake Alldredge and Daniel Craig. Our objective is to make and Amazon Alexa skill that interfaces with FamilySearch to collect and upload oral histories via Amazon Echo devices.

The oral-history will be the portion of our project that interacts with Alexa directly. User will dictate an oral history which Alexa
will then record and upload to FamilySearch.

# Our Stack
### Development Environment/ Tools
 - IntelliJ IDEA
 - Java
 - Node.js
 - Amazon Echo Dot (2nd Gen)
 - Amazon Web Services (AWS)
   - Free for the first year
   - Free up to 5000 speech requests per month
   - Lambdas
     - Event driven code
   - Kinesis Fire Hose
 - Family Search APIs

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
| IAM        | Identity and access management.  Where AWS permissions are managed.  |
| Intent     |            |
| Invoke     | The canonical term for starting the exection of a Lambda function    |
| Lambda     | A function that runs on AWS Lambda; no need for server config, etc.  |
| Sample     |            |
| Slot       |            |
| SSML       |            |
