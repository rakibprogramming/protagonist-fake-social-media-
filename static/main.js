function gotoPage(url) {
  if (typeof aiintval !== "undefined") {
    clearInterval(aiintval);
    console.log("cleared interval");
  }
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
  console.log(postData)
  if (postData != "" || !document.getElementById("previewImage").src.includes("/static/selectImage.png")) {
    document.getElementById('postThecontentButton').style.display = "none";
    document.getElementById('loadingbarforPost').style.display = "flex";
    let roating = 0;
    let loadingscreenInter = setInterval(() => {
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
      .then(response => response.json())
      .then(data => {
        document.getElementById('loadingbarforPost').style.display = "none";
        console.log("it is not")
        if (data.id != "error") {
          clearInterval(loadingscreenInter)
          gotoPage(`/post/${data.id}`)
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
}

window.addEventListener('popstate', function (event) {
  gotoPage(window.location.href)
});

function renderPost(username, userid, caption, hasimage, postid) {
  post = `
  <div class="posts">
                <div class="creatorInfo">
                    <img src="https://pub-6f9406fdeb2544f7acb2423deb3f6e1b.r2.dev/profileIcons/${userid}.jpg" alt="">
                    <div class="creatorTextInfo">
                        <span class="postCreatorNameinPost">${username}</span><br>
                        <span class="creationTimeofThepost">3 hours ago</span>
                    </div>
                </div>
                <div class="caption">
                    <span>${caption}</span>
                </div>
                ${hasimage == "0" ? '' :
      `<div class="imageFrame"><img src="https://pub-6f9406fdeb2544f7acb2423deb3f6e1b.r2.dev/postImage/${postid}.jpg" alt=""></div>`
    }
                <div class="postItarection">
                    <div class="postInarectionItem"><img src="/static/comments.png" alt=""><span>24</span></div>
                    <div class="postInarectionItem"><img src="/static/likes.png" alt=""><span>423</span></div>
                </div>
                <div class="commentsItarections">
                    <input type="text" placeholder="Add a comment...">
                </div>
    </div>
  `
  return post;
}
function getPost() {
  let lastId = document.getElementById("lastIdValue").value;
  document.getElementById("lastIdValue").remove();

  let paretn = document.getElementById("content");
  paretn.insertAdjacentHTML("beforeend", '<div id="postLoadingWating"><img id="postLoadingWatingImage" src="/static/loading.png" alt=""></div>')
  let roating = 0;
  let postLoadingInterval = setInterval(() => {
    document.getElementById("postLoadingWatingImage").style.rotate = `${roating}deg`;
    roating = roating + 3;
  }, 10);
  let formData = new FormData();
  formData.append("lastId", lastId)
  const csrftoken = getCookie('csrftoken');
  fetch("/getpost", { method: "POST", headers: { 'X-CSRFToken': csrftoken }, credentials: "same-origin", body: formData }).then(r => r.text()).then(data => {
    let contentparent = document.getElementById("content")
    contentparent.insertAdjacentHTML("beforeend", data)
    clearInterval(postLoadingInterval);
    document.getElementById("postLoadingWating").remove();
    requestRunning = false;

  }).catch((error) => console.error('Error:', error))
}


function addingComment(event, id) {
  event.preventDefault();

  let input = document.getElementById(id);
  let commentText = input.value;
  const formdata = new FormData();
  formdata.append("commentText", commentText);
  formdata.append("postId", id);

  const csrftoken = getCookie("csrftoken");
  fetch("/addcomment", {
    method: "POST",
    headers: {
      'X-CSRFToken': csrftoken,
    },
    credentials: 'same-origin',
    body: formdata,
  }).then(resp => resp.text()).then(data => {
    console.log("Comment added:", data);
    input.value = "";
  }).catch(error => console.error('Error:', error));

  return false;
}



function sendAddingLikeRequest(id) {
  let likeIMGelement = document.getElementById(id + "LIKE")
  if (likeIMGelement.src.includes("/static/likes.png")) {
    const csrftoken = getCookie("csrftoken");
    let formData = new FormData();
    formData.append("postID", id);
    fetch("/addlike", { method: "POST", headers: { 'X-CSRFToken': csrftoken }, credentials: "same-origin", body: formData }).then(res => res.text()).then(data => console.log(data)).catch(er => console("FUCK"))
    likeIMGelement.src = "/static/liked.png";
    let NumOfLike = document.getElementById(id + "LIKECOUNT").innerText;
    NumOfLike = Number(NumOfLike);
    document.getElementById(id + "LIKECOUNT").innerText = NumOfLike + 1;
  } else {
    const csrftoken = getCookie("csrftoken");
    let formData = new FormData();
    formData.append("postID", id);
    formData.append("remove", id);
    fetch("/addlike", { method: "POST", headers: { 'X-CSRFToken': csrftoken }, credentials: "same-origin", body: formData }).then(res => res.text()).then(data => console.log(data)).catch(er => console("FUCK"))
    likeIMGelement.src = "/static/likes.png";
    let NumOfLike = document.getElementById(id + "LIKECOUNT").innerText;
    NumOfLike = Number(NumOfLike);
    document.getElementById(id + "LIKECOUNT").innerText = NumOfLike - 1;
  }
}



function postLoading() {
  let paretn = document.getElementById("content");
  paretn.insertAdjacentHTML("beforeend", '<div id="postLoadingWating"><img id="postLoadingWatingImage" src="/static/loading.png" alt=""></div>')
  let roating = 0;
  setInterval(() => {
    document.getElementById("postLoadingWatingImage").style.rotate = `${roating}deg`;
    roating = roating + 3;
  }, 10);

}
