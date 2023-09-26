// include https://code.jquery.com/jquery-3.6.0.min.js



$(document).ready(function() {
    //declare the presignedUrlvariable
    let presignedUrl;
    let api_backend_url = "https://d5iwx94bq5.execute-api.us-east-1.amazonaws.com/prod/";
    let cognito_url = "https://cw-ws-78e52dcb-30dd-447f-bcc3-da13985e7c24.auth.us-east-1.amazoncognito.com/login?client_id=5n5rbs4gkle5e71g71ef3i3qa2&response_type=token&redirect_uri=https://d20dpssbjhqjf7.cloudfront.net/index.html";
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
    // a function that uploads a file to an s3 bucket that receives a signed url and return true if success and false otherwise
    function uploadFile(signedUrl="https://some.s3.amazonaws.com/") {
        // get the file from the input element
        const file = document.getElementById("image-upload").files[0];
        // get the file name
        const fileName = file.name;
        // get the file type
        const fileType = file.type;
        // get the file size
        const fileSize = file.size;
        // get the file data
        const fileData = new FormData();
        fileData.append("file", file);
        // get the presigned url
        const presignedUrl = signedUrl;
        // get the headers
        const headers = {
            "Content-Type": "application/json",
            "Content-Length": fileSize
        }
        // make the post request
        return post(presignedUrl, fileData, headers);
    
        
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
    // a function called get_presigned_url that receive id_token and generate a presigned url for S3 to upload a file to a s3 bucket
    function get_presigned_url(id_token) {
        // create a header for authorizartion with id_token
        const headers = {
            Authorization: `Bearer ${id_token}`
        }
        //make a reqquest to the api endpoint /api_backend and put it in a response
        return get(api_backend_url+"/api_backend_get", headers).then(response => {
            return response;
        });
    }
    // a function called submit_button_function(id_token)
    // that does call get_presigned_url(id_token) to get a presigned url from the api
    // then call uploadFile(presignedUrl) to upload the file to the presigned url
    function submit_button_function(id_token) {
        // create a header for authorizartion with id_token
        const headers = {
            Authorization: `Bearer ${id_token}`
        }
        // show the loading overlay
        showLoadingOverlay();
        // get a presigned url from the api
        get_presigned_url(id_token).then(response => {
            // store the presigned url in a global mutable variable
            presignedUrl = response;
        });
        // upload the file to the presigned url
        uploadFile(presignedUrl);
        // hide the loading overlay
        hideLoadingOverlay();
        // redirect to cognito
        window.location.href = cognito_url;
    }
    // a function that loads cognito credentials for an api request
    function loadCredentials() {
        return new Promise((resolve, reject) => {
            // get the id_token from the query string
            const id_token = window.location.hash.match(/id_token=([^&]+)/);
            // check if id_token has [1] index
            if(typeof id_token[1] === 'undefined') {
                reject(cognito_url);
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
        window.location.href = cognito_url;
    }

});