let top_bar = false;
toggle_top_bar();

window.addEventListener('scroll', function () {
    if (window.innerWidth < 1260 && top_bar) {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementsByClassName("top-bar")[0].style.top = "0";
        } else {
            document.getElementsByClassName("top-bar")[0].style.top = "-50px";
        }
    }
});

function toggle_top_bar () {
    if ((this.innerHeight <= 700 || this.innerWidth <= 1260)) {
        if (!top_bar) {
            Array.prototype.forEach.call(this.document.getElementsByClassName("navigation"), function (element) {
                element.classList.add("top-bar");
            });
            top_bar = true;
        }
    } else {
        Array.prototype.forEach.call(this.document.getElementsByClassName("navigation"), function (element) {
            element.classList.remove("top-bar");
            element.style.top = null;
        });
        top_bar = false;
    }
}

window.addEventListener('resize', toggle_top_bar);
