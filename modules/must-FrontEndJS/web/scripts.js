// include https://code.jquery.com/jquery-3.6.0.min.js



$(document).ready(function() {
    //declare the presignedUrlvariable
    let presignedUrl;
    let api_backend_url = "{replace_with_api_back_rul}";
    let cognito_url = "{replace_with_cognito_url}";
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
    // a function that ...
    function uploadFile(signedUrl="https://some.s3.amazonaws.com/") {
        // get the file from the input element
        const file = document.getElementById("file-input").files[0];
        // upload the file to the presigned url
        return new Promise((resolve, reject) => {
            $.ajax({
                url: signedUrl,
                type: 'PUT',
                data: file,
                processData: false,
                contentType: false,
                success: function(data) {
                    resolve(data);
                },
                error: function(error) {
                    reject(error);
                }
            })});
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
    // a function that ...
    function get_presigned_url(id_token) {
        // get the presigned url from the api
        return get(api_backend_url, {
            'Authorization': 'Bearer ' + id_token
        }).then(response => {
            // return the presigned url
            return response.presignedUrl;
        });
    }

    // a function that ...
    function submit_button_function(id_token){
        // show the loading overlay
        showLoadingOverlay();
        uploadFile(presignedUrl).then(response => {
            // hide the loading overlay
            hideLoadingOverlay();
            // get the response from the api
            return post(api_backend_url, {
                'Authorization': 'Bearer ' + id_token
            });
        });
        // hideLoadingOverlay();
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
