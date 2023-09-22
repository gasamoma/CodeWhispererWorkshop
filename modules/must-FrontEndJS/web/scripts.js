// include https://code.jquery.com/jquery-3.6.0.min.js



$(document).ready(function() {
    //declare the presignedUrlvariable
    let presignedUrl;
    const loadingOverlay = $("#loading-overlay");
    // get the id="submit-button" element
    const submitButton = $("#submit-button");
    // Function to show the loading overlay
    function showLoadingOverlay() {
        loadingOverlay.show();
    }

    // Function to hide the loading overlay
    function hideLoadingOverlay() {
        loadingOverlay.hide();
    }
    // a function that takes an s3 signed url as a parameter and uses it to upload a file. 
    function uploadFile(signedUrl="https://some.s3.amazonaws.com/") {
        // get the file from the input
        const file = $("#image-upload")[0].files[0];
        // make a request to the signed url
        $.ajax({
            contentType: 'binary/octet-stream',
            url: signedUrl,
            type: 'PUT',
            data: file,
            processData: false
        });
    }
    hideLoadingOverlay();
    // Call the showLoadingOverlay function when you want to display the overlay
    // Call the hideLoadingOverlay function when your
    
    // a fucntion that does a jquery post
    function post(url, data, headers={}) {
        return $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(data),
            dataType: 'json',
            headers: headers
            }
        );
    }
    // a fucntion tha does a jquery get.
    function get(url, headers={}) {
        return $.ajax({
            type: 'GET',
            url: url,
            headers: headers
        });
    }
    // a function that uses get to get the presigned url from this api https://pse9phfk51.execute-api.us-east-1.amazonaws.com/prod/api_backend and receives the id_token
    function get_presigned_url(id_token) {
        // create a header Authorization with the id_token
        headers = {
            'Authorization': 'Bearer ' + id_token
        }
        // do a get request to this endpoint /get_presigned_url
        return get('https://pse9phfk51.execute-api.us-east-1.amazonaws.com/prod/api_backend', headers).then(response => {
            // and return the presigned url
            return response;
        });
    }
    function submit_button_function(id_token){
        // show the loading overlay
        showLoadingOverlay();
        // upload the file to the presigned url using uploadFile
        uploadFile(presignedUrl['presigned_url']);
        // create a header Authorization with the id_token
        headers= {
             'Authorization': 'Bearer '+id_token
         }
        // get the object key from the presignedUrl['presigned_url']
        const objectKey = presignedUrl['presigned_url'].split('?')[0].split('/').pop();
        // do a post request to this endpoint /get_user_files
        post('https://pse9phfk51.execute-api.us-east-1.amazonaws.com/prod/api_backend',{'key':objectKey}, headers).then(response => {
            console.log(response);
            hideLoadingOverlay();
            
        });
    }
    // a function that loads cognito credentials for an api request
    function loadCredentials() {
        return new Promise((resolve, reject) => {
            // get the id_token from the query string
            const id_token = window.location.hash.match(/id_token=([^&]+)/);
            // check if id_token has [1] index
            if(typeof id_token[1] === 'undefined') {
                reject("https://cw-workshop-domain-demo.auth.us-east-1.amazoncognito.com/login?client_id=597e5f4rfac3sprtrd943h8jdg&response_type=token&redirect_uri=https://d2mj6f7u00o6eq.cloudfront.net/index.html");
            }
            // otherwise, resolve with the id_token
            resolve(id_token[1]);
        });
    }
    
    // if id_token is present in the query string
    if (window.location.hash.includes('id_token')) {
        // get a pressigned url from the api
        loadCredentials().then(id_token => {
            get_presigned_url(id_token).then(response => {
                // store the presigned url in a global mutable variable
                presignedUrl = response;
            });
        });
        submitButton.click(function() {
            loadCredentials().then(id_token => {
                // do a post with the credentials to the api
                submit_button_function(id_token);
            });
        });
    }else {
        window.location.href = "https://cw-workshop-domain-demo.auth.us-east-1.amazoncognito.com/login?client_id=597e5f4rfac3sprtrd943h8jdg&response_type=token&redirect_uri=https://d2mj6f7u00o6eq.cloudfront.net/index.html"
    }

});