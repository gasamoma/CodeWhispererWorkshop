// include https://code.jquery.com/jquery-3.6.0.min.js



$(document).ready(function() {
    // Document selection functionality
    const documentDropdown = $("#document-dropdown");
    // Search functionality
    const searchButton = $("#search-button");
    const searchInput = $("#search-input");
    const searchResultsContainer = $("#search-results-container");
    searchResultsContainer.hide();
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

    // a fucntion called populateDocumentDropdown that recienves a file list and adds it to the dropdown menu
    function populateDocumentDropdown(fileList) {
        documentDropdown.empty();
        for (let i = 0; i < fileList.length; i++) {
            const file = fileList[i];
            documentDropdown.append(new Option(file, file));
        }
    }


    searchButton.click(function() {
        const searchText = searchInput.val();
        // do a api request to : 'https://grl6bha8b4.execute-api.us-east-1.amazonaws.com/prod/query_bedrock'
        // create a
        post('https://grl6bha8b4.execute-api.us-east-1.amazonaws.com/prod/query_bedrock', {
            'query': searchText,
            // get the selected document from the dropdown menu
            'key': documentDropdown.val(),

        }).then(response => {
            // show the response in the in the search results container
            
            searchResultsContainer.empty();
            searchResultsContainer.show();
            searchResultsContainer.text(response);
        });

    });

    // Display search results
    function displaySearchResults(results) {
        searchResultsContainer.empty();
        
        searchResultsContainer.show();
        

        if (results && results.length > 0) {
            const ul = $("<ul>");
            results.forEach(result => {
                const li = $("<li>").text(result);
                ul.append(li);
            });
            searchResultsContainer.append(ul);
        }
        else {
            searchResultsContainer.text('No results found.');
        }
    }
    const loginButton = $("#login-button");
    const documentSelection = $("#document-selection");
    const openDocumentButton = $("#open-document-button");
    const searchContainer = $("#search-container");
    // Open selected document
    openDocumentButton.click(function() {
        searchContainer.show();
    });
    function login_button_fucntion(id_token){
        console.log("finished loading")
        // create a header Authorization with the id_token
        headers= {
             'Authorization': 'Bearer '+id_token
         }
        // do a post request to this endpoint https://grl6bha8b4.execute-api.us-east-1.amazonaws.com/prod/get_user_files
        post('https://grl6bha8b4.execute-api.us-east-1.amazonaws.com/prod/login',{}, headers).then(response => {

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
            const id_token = window.location.hash.match(/id_token=([^&]+)/)[1];
            // if there is no id_token, reject
            if (!id_token) {
                reject();
            }
            // otherwise, resolve with the id_token
            resolve(id_token);
        });
    }
    
    // if id_token is present in the query string
    if (window.location.hash.includes('id_token')) {
        // show the search container
        loadCredentials().then(id_token => {
            // do a post with the credentials to the api
            login_button_fucntion(id_token);
        });
    }
    // Amazon Cognito login functionality
    loginButton.click(function() {
        loadCredentials().then(id_token => {
            // do a post with the credentials to the api
            login_button_fucntion(id_token);
        });
    });
    
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
    
    
    
    // a fucntion tha does a jquery get.
    //function get(url) {
    //    return $.ajax({
    //        type: 'GET',
    //        url: url
    //    });
    //}
    
    // call the apigateway to get a signed url. 
    //function getSignedUrl(fileName) {
        // do a post request to the api
        //return get('https://grl6bha8b4.execute-api.us-east-1.amazonaws.com/prod/get_signed_url');
    //}
    
 
 
    
    
});