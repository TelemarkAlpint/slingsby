(function ($, window) {
    "use strict";

    moment.lang("nb");
    function improveTimestamps() {
        $('.isotimestamp').each(function () {
            var timestamp = $(this).attr('data-timestamp');
            var m = moment(timestamp);
            $(this).html(m.calendar());
            $(this).css("opacity", 1);
            $(this).attr("title", m.format("LLL"));
        });
    }

    window.improveTimestamps = improveTimestamps;

})(jQuery, this);
