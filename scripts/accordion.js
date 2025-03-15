var accordion = document.getElementsByClassName("accordion");

for (var i = 0; i < accordion.length; i++) {
    accordion[i].addEventListener("click", function () {
        var collapse = this.parentElement.nextElementSibling;
        this.parentElement.classList.toggle("open");

        if (collapse.style.maxHeight) {
            collapse.style.transitionDuration = "0.25s";
            collapse.style.maxHeight = null;
        } else {
            collapse.style.transitionDuration = Math.max(collapse.scrollHeight / 1500, 0.25) + "s";
            collapse.style.maxHeight = collapse.scrollHeight + "px";
        }
    });

    // Observe changes in size (including dynamic content like images)
    var content = accordion[i].parentElement.nextElementSibling;
    var resizeObserver = new ResizeObserver(() => {
        if (content.style.maxHeight) {
            content.style.transitionDuration = "0";
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });

    resizeObserver.observe(content);
}