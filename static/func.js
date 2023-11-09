window.addEventListener("DOMContentLoaded", (event) => {
    const actualBtn = document.getElementById("real-button");
    const fileChosen = document.getElementById("file-chosen");
    actualBtn.addEventListener("change", 
        function () {
        fileChosen.textContent = this.files[0].name;
        }
    );
});