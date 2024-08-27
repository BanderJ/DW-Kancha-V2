document.getElementById("user-dropdown-button").onclick = function() {
    var content = document.getElementById("user-dropdown-content");
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
};

window.onclick = function(event) {
    if (!event.target.matches('#user-dropdown-button')) {
        var dropdowns = document.getElementsByClassName("user-dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
};