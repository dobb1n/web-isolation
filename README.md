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
- vt returned data now updates the web request it came from 

## todo
- check db rules
- have front end subscribe to doc to get updated
