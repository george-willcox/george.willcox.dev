window.dispatchEvent(new Event('scroll'));  // Just to make sure styling is correct if page is refreshed

window.addEventListener('scroll', function () {
    if (window.innerWidth < 1260 || this.window.innerHeight < 700) {
        let navigation = document.getElementsByClassName('navigation')[0];
        let elements = navigation.getElementsByTagName("li");
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            navigation.style.backgroundColor = '#444';
            navigation.style.color = 'white';
            navigation.style.boxShadow = '0 4px 12px 0 rgba(0, 0, 0, 0.3)';
            Array.from(elements).forEach(element => {
                element.style.padding = '20px 10px';
                element.style.fontSize = '1.2rem';
            });
        } else {
            navigation.style = null;
            Array.from(elements).forEach(element => {
                element.style = null;
            });
        }
    }
});

window.addEventListener('resize', function () {
    if (window.innerWidth >= 1260 && window.innerHeight >= 700) {
        let navigation = document.getElementsByClassName('navigation')[0];
        navigation.style = null;
    }
});
