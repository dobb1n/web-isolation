# web isolation risk detector

this is the definition of a firebase app which authenticates a user to a front end and accepts a URL from them which it goes off and checks against virustotal. other checks to be incorporated. 

## how to update it
if you merge into main a github action deploys to firebase hosting
you will need to manually deploy the functions : 

`firebase deploy --only functions`

this updates : https://web-isolation-risk.web.app/

## working
- front end auth
- execution of cloud function on new doc creation


## todo
- check db rules
- do something better with the virustotal data returned - i.e update status, and when status changes to completed, then go off and run the decision engine. 
- store it in the right collection
- have front end subscribe to doc to get updated
