(function ($) {
    "use strict";

    function countdownToSignup() {
        var secondsRemaining = parseInt($('.event').attr('data-time-remaining-to-signup-opens'), 10);
        if (secondsRemaining > 0) {
            var countdown = setInterval(function () {
                if (secondsRemaining <= 0) {
                    clearInterval(countdown);
                    location.reload(true);
                } else if (secondsRemaining < 1800) {
                    if (secondsRemaining % 180 === 0 && secondsRemaining >= 120) {
                        history.go(0);
                    }
                    var minutesRemaining = Math.floor(secondsRemaining / 60);
                    var text = secondsRemaining % 60 + 's';
                    text = minutesRemaining > 0 ? minutesRemaining + ' min og ' + text : text;
                    $("span.countdown").html(' (om ' + text + ')');
                }
                secondsRemaining--;
            }, 1000);
        }
    }
    countdownToSignup();

})(jQuery);
