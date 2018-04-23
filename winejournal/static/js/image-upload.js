
function fileSelected() {
    var file = document.getElementById('image').files[0];
    if (file) {
        var fileSize = 0;
        if (file.size > 1024 * 1024)
            fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
        else
            fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

        document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
        document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
        document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
        showFile();
        // getSignedRequest(file)
    }
}

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

function showFile() {
    var fileInput = document.getElementById('image');
    var fileDisplayArea = document.getElementById('thumbnail');
    var wineMeta = document.getElementById('wine-meta');
    console.log(fileInput)

    console.log('it changed')
    var file = fileInput.files[0];
    var imageType = /image.*/;

    if (file.type.match(imageType)) {
        var reader = new FileReader();

        reader.onload = function (e) {
            fileDisplayArea.innerHTML = "";

            // Create a new image.
            var img = new Image();
            // Set the img src property using the data URL.
            img.src = reader.result;
            img.setAttribute("width", "100%");
            img.setAttribute("height", "auto%");

            // Add the image to the page.
            fileDisplayArea.appendChild(img);
            fileDisplayArea.style.display = 'block';
            wineMeta.style.display = 'block';
        }

        reader.readAsDataURL(file);
    } else {
        fileDisplayArea.innerHTML = "File not supported!";
    }

}

function removeImage() {
    var file = document.getElementById('image');
    var hidden = document.getElementById('delete_image');
    var fileDisplayArea = document.getElementById('thumbnail');
    var wineMeta = document.getElementById('wine-meta');
    file.value = '';
    hidden.value = "true"
    fileDisplayArea.innerHTML = "";
    fileDisplayArea.style.display = 'none';
    wineMeta.style.display = 'none';
    document.getElementById('fileName').innerHTML = '';
    document.getElementById('fileSize').innerHTML = '';
    document.getElementById('fileType').innerHTML = '';
}

function imageRotateLeft() {
    var image = document.getElementById('thumbnail');
    var rotateField = document.getElementById('rotate_image')
    image.style.WebkitTransform = "rotate(0deg)";
    image.style.WebkitTransform = "rotate(-90deg)";
    image.style.transform = "rotate(0deg)";
    image.style.transform = "rotate(-90deg)";
    rotateField.value = "90"
}

function imageRotateRight() {
    var image = document.getElementById('thumbnail');
    var rotateField = document.getElementById('rotate_image')
    image.style.WebkitTransform = "rotate(0deg)";
    image.style.WebkitTransform = "rotate(90deg)";
    image.style.transform = "rotate(0deg)";
    image.style.transform = "rotate(90deg)";
    rotateField.value = "270"
}

function imageRotate180() {
    var image = document.getElementById('thumbnail');
    var rotateField = document.getElementById('rotate_image')
    image.style.WebkitTransform = "rotate(0deg)";
    image.style.WebkitTransform = "rotate(180deg)";
    image.style.transform = "rotate(0deg)";
    image.style.transform = "rotate(180deg)";
    rotateField.value = "180"

}