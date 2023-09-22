# Welcome to youd Code Whisperer module Cognito Security

---
## Your tasks:

### File app/lambda/post_auth.py
get_presigned_url(id_token)
#### Input
_id_token_ : This is the Bearer id_token from cognito. It does not contain the "bearer " part

#### Output
Response from the api_get lambda function response from API GateWay

### File app/lambda/post_auth.py

handler(event, context)

#### Input
_event_ : A Cognito post authorization lambda invocation Event.
_context_ : A Cognito post authorization lambda invocation context.
#### Output
Store in the Dynamo DB table the email of the user with the current timestamp

### File app/security/security.py
check_auth(event)
#### Input
event : A Api Gateway Lambda proxy event(POST)
#### Output
True if POST_AUTH is == "1" and if there is any authentication within the last hour from the user in dynamoDb
False Any other scenario

You have the following Table schema 
* 'user-email': 'S',
* 'date': 'S'

# Welcome to your CDK Python project!

This is a project for CDK development with Python.

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

```
$ cdk bootstrap
```


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
