(function ($) {
    "use strict";

    //Navigation

    var app = function () {
        var body = undefined;
        var menu = undefined;
        var menuItems = undefined;
        var init = function init() {
            body = document.querySelector('body');
            menu = document.querySelector('.menu-icon');
            menuItems = document.querySelectorAll('.nav__list-item');
            applyListeners();
        };
        var applyListeners = function applyListeners() {
            menu.addEventListener('click', function () {
                return toggleClass(body, 'nav-active');
            });
        };
        var toggleClass = function toggleClass(element, stringClass) {
            if (element.classList.contains(stringClass)) element.classList.remove(stringClass); else element.classList.add(stringClass);
        };
        init();
    }();


    //Switch light/dark

    if (localStorage.getItem("darkMode") == "disabled") {
        $("body").addClass("light");
        $("#switch").addClass("switched");
    }

    $("#switch").on('click', function () {
        if ($("body").hasClass("light")) {
            $("body").removeClass("light");
            $("#switch").removeClass("switched");
            localStorage.setItem("darkMode", "enabled");
        }
        else {
            $("body").addClass("light");
            $("#switch").addClass("switched");
            localStorage.setItem("darkMode", "disabled");
        }
    });

    //music player: autoplay on click (link to an audio html tag with id = player)

    // document.addEventListener('click', musicPlay);
    // function musicPlay() {
    //     var audio = document.getElementById("player");
    //     audio.play();
    //     audio.volume = 0.1;
    //     document.removeEventListener('click', musicPlay);
    // }


})(jQuery);
