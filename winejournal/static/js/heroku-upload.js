// This is a slightly modified version of Heroku's suggested javascript client
// It can be called from fileSelected() and works to upload an unedited
// version of the image to S3.  It is not being used but is retained here for
// future reference


function getSignedRequest(file){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/s3/sign-s3?file_name="+file.name+"&file_type="+file.type);
  xhr.onreadystatechange = function(){
    if(xhr.readyState === 4){
      if(xhr.status === 200){
        var response = JSON.parse(xhr.responseText);
        uploadFile(file, response.data, response.url);
      }
      else{
        alert("Could not get signed URL.");
      }
    }
  };
  xhr.send();
}

function uploadFile(file, s3Data, url){
  var xhr = new XMLHttpRequest();
  var imageURL = document.getElementById('image_url')
  xhr.open("POST", s3Data.url);
console.log(s3Data, url)
  var postData = new FormData();
  for(key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4){
      if(xhr.status === 200 || xhr.status === 204){
        document.getElementById("image").setAttribute('data-url', url);
        imageURL.value = url;
      }
      else{
        alert("Could not upload file.");
      }
   }
  };
  xhr.send(postData);
}