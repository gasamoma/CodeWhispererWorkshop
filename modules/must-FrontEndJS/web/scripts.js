
//a variable that captures the value of a input field called access - code
const accessCode = $("#access-code");
const apiurl = 'https://1236546123.execute-api.us-east-1.amazonaws.com/prod/api_backend';
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
