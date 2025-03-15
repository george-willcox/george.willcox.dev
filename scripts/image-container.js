document.querySelectorAll('.image-container').forEach(container => {
    const images = container.querySelectorAll('img');

    let touchStartX = 0;
    let touchStartY = 0;

    function toggleSize(clickedImg) {
        if (clickedImg.classList.contains("large")) {
            // Reset both to equal size
            images.forEach(img => {
                img.classList.remove("large", "small");
            });

        } else {
            console.log("togged")
            // Make clicked image large and the other small
            images.forEach(img => {
                img.classList.toggle("large", img === clickedImg);
                img.classList.toggle("small", img !== clickedImg);
            });
        }
    }

    images.forEach(img => {
        img.addEventListener("mouseenter", function () {
            toggleSize(this);
        });

        img.addEventListener("touchstart", function (e) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        });

        img.addEventListener("touchend", function (e) {
        // Only trigger the toggle size logic if there was no significant movement (indicating a tap)
        const touchMoveX = e.changedTouches[0].clientX;
        const touchMoveY = e.changedTouches[0].clientY;

        // If the movement was small (i.e., a tap), trigger toggleSize
        if (Math.abs(touchMoveX - touchStartX) <= 10 && Math.abs(touchMoveY - touchStartY) <= 10) {
            toggleSize(this);
        }
    });
    });
});