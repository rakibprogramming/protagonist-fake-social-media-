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




