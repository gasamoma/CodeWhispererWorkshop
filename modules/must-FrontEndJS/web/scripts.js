//a variable that captures the value of a input field called access - code
const accessCode = $("#access-code");
const apiurl = 'https://1236546123.execute-api.us-east-1.amazonaws.com/prod/api_backend';
var bucketName = "cw-workshop";
var bucketRegion = "us-east-1";
var IdentityPoolId = "1234567890";

<<<<<<< HEAD
//extract token from web url querystring parameters and assign it to a variable called token 
const token = new URLSearchParams(window.location.search).get('token');
=======
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
>>>>>>> 7c027f0bfa60450b0b8706bff9b18e54a11bc5f8


//A function that validates a cognito jwt tokenken

function validateJWTToken(token) {
    var url = apiurl + '/validate';
    var headers = {
        'Authorization': 'Bearer ' + token
    };
    return post(url, {}, headers);
}



//a function that takes the value of the access code and sends it to the api endpoint  and returns the response as a json object
 function post(url, data, headers = {}) {
     return $.ajax({
         type: 'POST',
         url: url,
         data: JSON.stringify(data),
         dataType: 'json',
         headers: JSON.stringify(headers)
     });
 }
 
 // a function that uploads a file using aws sdk

 
function s3upload() {  
        var files = document.getElementById('fileUpload').files;
        if (files) 
        {
            var file = files[0];
            var fileName = file.name;
            var filePath = 'my-first-bucket-path/' + fileName;
            var fileUrl = 'https://' + BUCKET_REGION + '.amazonaws.com/my-first-bucket/' +  filePath;
            
<<<<<<< HEAD
            s3.upload({
                        Key: filePath,
                        Body: file,
                        ACL: 'public-read'
                     }, function(err, data) {
                         if(err) {
                            reject('error');
                         }
                                    
                        alert('Successfully Uploaded!');
                    }).on('httpUploadProgress', function (progress) {
                        var uploaded = parseInt((progress.loaded * 100) / progress.total);
                        $("progress").attr('value', uploaded);
                    });
                }
      };
=======
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
});
>>>>>>> 7c027f0bfa60450b0b8706bff9b18e54a11bc5f8
