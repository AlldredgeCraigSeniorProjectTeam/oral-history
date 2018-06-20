![Project Logo](header.png)
###### Contributors: Jacob Alldredge and Daniel Craig

### Summary
This is the senior project repo of Jake Alldredge and Daniel Craig. Our objective is to make and Amazon Alexa skill that interfaces with FamilySearch to collect and upload oral histories via Amazon Echo devices.

## Development Environment/ Tools
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

## Skills
 - Dictation of family history
 - Family memory retrieval and read

## Authentication
 - Link amazon and FamilySearch?
   - Web application

## Workflow
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

# Define

| Term       | Definition |
| IAM        |            |
| Intent     |            |
| Invocation |            |
| Lambda     |            |
| Sample     |            |
| Slot       |            |
| SSML       |            |
|            |            |

# Hello World

## arn:aws:lambda:us-east-1:545339878944:function:HelloWorld


# Clock

| Date     | Description                | Time | PP |
|----------|----------------------------|------|----|
| 05/07/18 | Ideas                      | 0:39 | X  |
| 05/08/18 | "                          | 0:17 | X  |
| 05/09/18 | "                          | 0:11 | X  |
| "        | "                          | 0:11 | X  |
| "        | Workflow                   | 0:35 | X  |
| "        | Environment setup          | 0:35 | X  |
| "        | Cleaned up md              | 0:38 | X  |
| "        | Structured directories     | 1:32 | X  |
|          | Total                      | 8:24 |    |
