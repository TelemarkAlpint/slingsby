(function ($) {
    "use strict";

    $(".social_summary_textbox").each(function () {
        $(this).after('<br><span>Antall tegn: 0</span>');
        $(this).keyup(function () {
            var length = this.value.length;
            $(this).siblings("span").html("Antall tegn: " + length);
        });
    });
}(jQuery));
