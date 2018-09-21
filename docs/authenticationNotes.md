# Notes from figuring out authentication with FamilySearch
So far this project has been a big learning opportunity re authentication, and I wanted to document the steps I took to figure out how to link an Alexa skill to a third-party service that we don't own, using OAuth 2.

We were pleasantly surprised to find that OAuth 2 makes it very straightforward to let users authorize Alexa to make FamilySearch API calls on their behalf.  Our skill's auth flow will first have users enter their FamilySearch credentials in the browser window that pops up with the LinkAccount card in the Alexa app.  The skill will then retrieve an authorization code from FamilySearch, which will allow API calls to be performed.  Through the API we will attach the user's stories to their family member's records on FamilySearch.

Authentication done via the method known as 'Authorization code grant' allows us to refresh the access code, making it so that API access is uninterrupted by expired credentials.

# Milestones, and the steps taken to accomplish them
## Milestone 1: Return a LinkAccount card to the Alexa app
### Steps:
1. Return a LinkAccount card.  This is achieved by returning simple JSON.  See the commit at https://github.com/AlldredgeCraigSeniorProjectTeam/oral-history/commit/370d693b5661bcab0820bd4f071ee4c19b8a6f05
2. Verify that the card is returned in the Alexa app.

## Configure Account Linking in the Alexa Skill and in the FamilySearch developer console
### Steps:
1. Register for a FamilySearch developer account.  See https://www.familysearch.org/developers/
2. Create a new app via My Apps > Create App.  Make sure that you set it as 'Web' application type.  The redirect URI's can be configured later.
3. Follow the following instructions to set up account linking with your Alexa skill and FamilySearch.  Doing this means that the LinkAccount card's 'Link Account' button will automatically go to FamilySearch's signin page. The Client Id needed by the Alexa skill is your FamilySearch-provided App Key found on your 'My Apps' tab, and the Client Secret is the password shown in the My Account > Integration (Sandbox) Account tab https://developer.amazon.com/blogs/post/Tx3CX1ETRZZ2NPC/Alexa-Account-Linking-5-Steps-to-Seamlessly-Link-Your-Alexa-Skill-with-Login-wit
4. Add 3 redirect URI's to your app's config on FamilySearch using the 3 Redirect URI's provided on the Account Linking portion of the Alexa Skill > Build dashboard.  These tell FamilySearch where to redirect to when the user logs in successfully.
5. Test the skill's ability to login by using the LinkAccount card and FamilySearch's login page to prompt the user for their credentials.
