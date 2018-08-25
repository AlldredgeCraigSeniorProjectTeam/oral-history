# Transcription Test Plan
The success of our project depends whether or not Amazon allows Alexa to post text data to services outside itself.  Our final product will need to transcribe voice input and post the text that that generates to FamilySearch.  This transcription test will test that this is possible.

# Milestones, and the steps taken to achieve them
## Milestone 1: Project successfully uses Alexa to transcribe a user story
### Steps:
1. Learn more about slots and evaluate how to solve the problem of 'listening' for the story that the user is telling.
2. Write the functionality that allows the skill to transcribe a user's oral history - to demonstrate this, have the skill repeat the user's story out loud

## Milestone 2: Project successfully posts user story to S3 
### Steps:
1. Learn how to post to S3 from Python and from inside the Lambda
2. Write the functionality that allows the skill to post the text from Milestone 1 to s3
