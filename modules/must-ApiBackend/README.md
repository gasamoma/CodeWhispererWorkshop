# Welcome to youd Code Whisperer module Api Backend

---
## Your tasks:

### File app/lambda/api.py
handler(event, context)
#### Input

_event_ : A Cognito post authorization lambda invocation Event.

_context_ : A Cognito post authorization lambda invocation context.

_event['body']['key']_ : the key of the uploaded S3 object
#### Output
Respond if the user is authorized or not to go to mars

To do so, you need to desing a challenging photo for the Mars Candidate 
traveler, either to have their mouth open, eyes closed or whatever you want to 
use in Rekognition DetectFaces.

The image to be analized is going to be uploaded to the Key destination of the 
OS environment variable bucket



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
