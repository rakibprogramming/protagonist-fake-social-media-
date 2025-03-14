function gotoPage(url) {
  const preloadCSS = document.createElement("link");
  preloadCSS.rel = "preload";
  preloadCSS.href = "/static/style.css";
  preloadCSS.as = "style";
  history.pushState(null, "", url);
  fetch(url)
    .then(response => response.text())
    .then(data => {
      document.open();
      document.write(data);
      document.close();
    })
    .catch(error => {
      console.error('Error:', error);
    });

  document.head.appendChild(preloadCSS);
  let html = document.getElementById("loadingScreenHtml").innerHTML;
  document.getElementById("loadingScreenHtml").innerHTML = "";
  document.getElementById('content').innerHTML = html;
  let roating = 0;
  setInterval(() => {
    document.getElementById("loadingScreenLoadingIcon").style.rotate = `${roating}deg`;
    roating = roating + 3;
  }, 10);
}



function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


var csrftoken = getCookie('csrftoken');

function sendData() {
  let postData = document.getElementById("postText").value;

  if (postData != "" || !document.getElementById("previewImage").src.includes("/static/selectImage.png")) {
    document.getElementById('postThecontentButton').style.display = "none";
    document.getElementById('loadingbarforPost').style.display = "flex";
    let roating = 0;
    setInterval(() => {
      document.getElementById("postLoadingImage").style.rotate = `${roating}deg`;
      roating = roating + 3;
    }, 10);

    console.log(document.getElementById("previewImage").src)
    const fileInput = document.getElementById('postImage');
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('postText', postData);
    formData.append('key2', 'value2');

    const csrftoken = getCookie('csrftoken');

    fetch('/validatedata', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      credentials: 'same-origin',
      body: formData,
    })
      .then(response => response.text())
      .then(data => {
        document.getElementById('loadingbarforPost').style.display = "none";
        console.log('Success:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
}

