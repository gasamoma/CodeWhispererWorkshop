//a variable that captures the value of a input field called access - code
const accessCode = $("#access-code");
const apiurl = 'https://1236546123.execute-api.us-east-1.amazonaws.com/prod/api_backend';
var bucketName = BUCKET_NAME;
var bucketRegion = BUCKET_REGION;
var IdentityPoolId = IDENTITY_POOL_ID;


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