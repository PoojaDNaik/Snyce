if(!localStorage.getItem("id")){
    window.location.pathname = '/login'
}

async function greet() {
    const response = await fetch("/userdetail/" + localStorage.getItem("id"));
    const res = await response.json();
    const head = document.getElementById("head");
    head.innerHTML = "Hii " + res.email;
    const myListLink = document.getElementById("myList");
    myListLink.setAttribute(
      "href",
      "/my-check-list/" + localStorage.getItem("id")
    );
}
greet();