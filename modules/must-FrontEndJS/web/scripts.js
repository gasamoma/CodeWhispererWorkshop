// include https://code.jquery.com/jquery-3.6.0.min.js



$(document).ready(function() {
    //declare the presignedUrlvariable
    let presignedUrl;
    const loadingOverlay = document.getElementById("loading-overlay");
    // get the id="submit-button" element
    const submitButton = document.getElementById("submit-button");
    // Function to show the loading overlay
    function showLoadingOverlay() {
        loadingOverlay.style.display = "block";
    }

    // Function to hide the loading overlay
    function hideLoadingOverlay() {
        loadingOverlay.style.display = "none";
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
    // a function that uses get to get the presigned url from this api https://gce33wbizd.execute-api.us-east-1.amazonaws.com/prod/api_backend and receives the id_token
    function get_presigned_url(id_token) {
        // create a header Authorization with the id_token
        headers = {
            'Authorization': 'Bearer ' + id_token
        }
        // do a get request to this endpoint /get_presigned_url
        return get('https://gce33wbizd.execute-api.us-east-1.amazonaws.com/prod/api_backend', headers).then(response => {
            // and return the presigned url
            return response;
        });
    }
    function submit_button_function(id_token){
        // show the loading overlay
        showLoadingOverlay();
        console.log("finished loading")
        // create a header Authorization with the id_token
        headers= {
             'Authorization': 'Bearer '+id_token
         }
        // do a post request to this endpoint /get_user_files
        post('https://gce33wbizd.execute-api.us-east-1.amazonaws.com/prod/api_backend',{}, headers).then(response => {

            // and get the list of files from the response
            const files = response;

            // populate the dropdown with the list of files
            populateDocumentDropdown(files);
            // show the document selection UI
            documentSelection.show();
            $("#login-container").hide();
            
        });
    }
    // a function that loads cognito credentials for an api request
    function loadCredentials() {
        return new Promise((resolve, reject) => {
            // get the id_token from the query string
            const id_token = window.location.hash.match(/id_token=([^&]+)/);
            // check if id_token has [1] index
            if(typeof id_token[1] === 'undefined') {
                reject("https://cw-workshop-demo-domain.auth.us-east-1.amazoncognito.com/login?client_id=2qkldhuvbk4ibcjg7q4dcdcde&response_type=token&redirect_uri=https://d2kbjcta2fltwo.cloudfront.net/index.html");
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
        // Amazon Cognito login functionality
        submitButton.click(function() {
            loadCredentials().then(id_token => {
                // do a post with the credentials to the api
                submit_button_function(id_token);
            });
        });
    }else {
        window.location.href = "https://cw-workshop-demo-domain.auth.us-east-1.amazoncognito.com/login?client_id=2qkldhuvbk4ibcjg7q4dcdcde&response_type=token&redirect_uri=https://d2kbjcta2fltwo.cloudfront.net/index.html"
    }
    
    
    //const signed="https://deepracer-destination.s3.amazonaws.com/"
    // a function that takes an s3 signed url as a parameter and uses it to upload a file. 
    function uploadFile(signedUrl="https://deepracer-destination.s3.amazonaws.com/") {
        // get the file from the input
        const file = $("#fileUpload")[0].files[0];
        // make a request to the signed url
        $.ajax({
            url: signedUrl,
            type: 'PUT',
            data: file,
            processData: false,
            contentType: false
        });
    }
    
    
    
    
    
    // call the apigateway to get a signed url. 
    //function getSignedUrl(fileName) {
        // do a post request to the api
        //return get('https://grl6bha8b4.execute-api.us-east-1.amazonaws.com/prod/get_signed_url');
    //}
    
 
 
    
    
});