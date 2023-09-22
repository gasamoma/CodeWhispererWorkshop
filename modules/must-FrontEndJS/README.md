# Welcome to youd Code Whisperer module

---
## Your tasks:

### File web/scripts.js
get_presigned_url(id_token)
#### Input
_id_token_ : This is the Bearer id_token from cognito. It does not contain the "bearer " part

#### Output
Response from the api_get lambda function response from API GateWay

### File web/scripts.js

submit_button_function(id_token)

#### Input
_id_token_ : This is the Bearer id_token from cognito. It does not contain the "bearer " part
#### Output
Show if the user is authorized to go to mars or not!

To do so, you should upload the image to s3, then you would need to call the api_backend to check if the used photo passed the test 

### File web/scripts.js
uploadFile(signedUrl)
#### Input
signedUrl : This is the s3 PUT Presingned URL
#### Output
True if success, False otherwhise

You have helper functions like 
* showLoadingOverlay
* hideLoadingOverlay
* post
* get
* loadCredentials

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
