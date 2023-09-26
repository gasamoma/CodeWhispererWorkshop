// include https://code.jquery.com/jquery-3.6.0.min.js



$(document).ready(function() {
    //declare the presignedUrlvariable
    let presignedUrl;
    let api_backend_url = "https://01qe0n5kdl.execute-api.us-east-1.amazonaws.com/prod/";
    let cognito_url = "https://cw-ws-fcceee3b-feb4-4018-883b-252db64a1c71.auth.us-east-1.amazoncognito.com/login?client_id=6hih9l82ni4h5102ui13hqmdid&response_type=token&redirect_uri=https://d1arscppw1i0hm.cloudfront.net/index.html";
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
    // a function that make a put to S3 presignedUrl and return true if success, otherwise false
    function uploadFile(presignedUrl) {
        // get the image
        const file = document.getElementById('image-upload').files[0];
        // get the image name
        const fileName = file.name;
        // get the image type
        const fileType = file.type;
        // get the image size
        const fileSize = file.size;
        // get the image
        const fileData = new FormData();
        fileData.append('file', file);
        // make the put request to S3
        return $.ajax({
            type: 'PUT',
            url: presignedUrl,
            data: fileData,
            processData: false,
            contentType: false,
            headers: {
                'Content-Type': fileType
            }
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
    // a function that call the api_get API Gateway
    function get_presigned_url(id_token) {
        return get(api_backend_url + '/api_backend', {
            'Authorization': 'Bearer ' + id_token,
            'Content-Type': 'application/json'
        });
    }

    function submit_button_function(id_token){
        // show the loading overlay
        showLoadingOverlay();
        // upload image to S3
        uploadFile(presignedUrl);
        
        // call the api_backend to check if the user is authorized to go to mars
        post(api_backend_url + '/api_backend', {
            'Authorization': 'Bearer ' + id_token,
            'Content-Type': 'application/json'
        }).then(response => {
            // check if the response is true
            if (response.data.is_valid) {
                // redirect to mars
                window.location.href = "index.html";
            } else {
                // redirect to not authorized
                //window.location.href = “not_authorized.html”;
                window.location.href = "error.html";
            }
        });
        hideLoadingOverlay();
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
