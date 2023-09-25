# CodeWhispererWorkshop

<h2 align="center">Today we are going to build! with AI!</h2>


## Contens

- 🔭 [Modules and architecture](#modules-and-architecture)

- 👤 [Start a new Workshop:](#how-to-start-a-new-workshop)

- 🚀 [Toolkit](#toolkit)


### Modules And Architecture
1. Please look at the must-modules architecture [Diagram](./architecture.jpg)
    
**Modules Readme.md:** 
* must-CognitoSecurity [.MD](./modules/must-CognitoSecurity/README.md)
* must-ApiBackend [.MD](./modules/must-ApiBackend/README.md)
* must-FrontEndJS[.MD](./modules/must-FrontEndJS/README.md)
* extra-LogForensis *WIP*
* extra-ProactiveLogAnalisys *WIP*
* extra-SecurityFindings *WIP*
* extra-unitTesting *WIP*

**IMPORTANT:** you are meant to code the function described in each module 
Readme, an automated CI/CD pipeline will attempt to deploy your application, 
be aware any changes made in the Javascript would probably need you to clear cache and hard Reload the website 


### How To start a new Workshop

![](./images/emailcode.png)


1. Run: `chmod +x ./code_manager/create_workshop.sh`
2. Run: `./code_manager/create_workshop.sh`
3. You are already working on your workshop branch, if not:
    1. `git branch -a`
    2. `git branch checkout -b ws/{$uuid}`

### Toolkit

#### 1. Usefull Git commands

- `git status` shows the changed files and the working branch
- `git diff {File/path}` shows what changed in a particular file directory or all changes
- `git add {.|File}` adds the file for a fowolling commit
- `git restore {.|File}` rolls back any changes until the last commit
- `git commit -m "{comment}"` packs all the tracked files changes into a commit with the comment
- `git push origin ws/{branch}` pushes the commits into the remote branch
- `git checkout {-b}` changes the current working branch {-b} for a new branch


#### 2. Activate code whisperer:

Code whisperer IDE Documentation [link](https://docs.aws.amazon.com/codewhisperer/latest/userguide/getting-started.html)

- Suggestions for promts:
    - Function oriented: think first of the desired task and what does the function need to do.
    - Dont try to generate the perfect code! You can always work with the base, and correct it when is needed with embbeded comments.
    - Stop trying to lookup for documentations, try to assume codewhisperer understands the response type/structure of certain libraries.

#### 3. Do NOT modify the stacks:
The infrastructure allready has a CI/CD and it's supposed to run on each push of your current Workshop branch
