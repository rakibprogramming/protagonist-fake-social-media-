function openAddingPost() {
    document.getElementById("addingpostArea").style.zIndex="20000";

    document.getElementById("addingpostArea").style.visibility="visible";
    document.getElementById("closingAdding").style.visibility="visible";

    document.getElementById("addingPost").style.opacity="1";
    document.getElementById("addingPostOverlay").style.opacity="1";
}

function closingAddingPost(){
    document.getElementById("addingPost").style.opacity="0";
    document.getElementById("addingPostOverlay").style.opacity="0";
    document.getElementById("closingAdding").style.visibility="hidden";

    setTimeout(() => {
        document.getElementById("addingpostArea").style.visibility="hidden";
    }, 200);
}
function fileSeceted(event) {
    const file = event.target.files[0]; // Get the selected file
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      
      // Event listener for when the file is successfully read
      reader.onload = function(e) {
        const imgElement = document.getElementById('imagePreview');
        imgElement.src = e.target.result; // Set the source of the image
      };
      
      // Read the selected file as a data URL
      reader.readAsDataURL(file);
    } else {
      alert('Please select an image file.');
    }
}
document.getElementById('adingImage').addEventListener('change', fileSeceted);


function changeUrl() {
  history.pushState(null, "", "/notification.html");
  fetch('/notification.html')
  .then(response => response.text())
  .then(data => {
    document.body.innerHTML=data;
  })
  .catch(error => console.error('Error:', error))
}