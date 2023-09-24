#!/bin/sh
uuid=$(uuidgen)
git checkout -b ws/$uuid
sed -e 's~"https://cw-workshop-domain-demo.auth.us-east-1.amazoncognito.com/login?client_id=597e5f4rfac3sprtrd943h8jdg&response_type=token&redirect_uri=https://d2mj6f7u00o6eq.cloudfront.net/index.html"~"{replace_with_cognito_url}"~g' -e 's~"https://pse9phfk51.execute-api.us-east-1.amazonaws.com/prod/api_backend"~"{replace_with_api_back_rul}"~g'  modules/must-FrontEndJS/web/scripts.bck.js > modules/must-FrontEndJS/web/scripts.js 
sed -e "s~cw-workshop-domain-demo~cw-ws-$uuid~g" modules/must-ApiBackend/must_api_backend/must_api_backend_stack.bck.py > modules/must-ApiBackend/must_api_backend/must_api_backend_stack.py
rm rf modules/must-FrontEndJS/web/scripts.bck.js modules/must-ApiBackend/must_api_backend/must_api_backend_stack.bck.py
git add .
git commit -m "first commit"
git push origin uuid
echo "git checkout -b ws/$uuid"