function toggleForm() {
    var form = document.getElementById("crea-evento-form");
    var overlay = document.getElementById("overlay");
    if (form.style.display === "none") {
        form.style.display = "block";
        overlay.style.display = "block";
    } else {
        form.style.display = "none";
        overlay.style.display = "none";
    }
}