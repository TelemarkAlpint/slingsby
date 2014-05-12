(function ($, moment) {
    "use strict";

    function countdownToSignup() {
        var signupTime = moment.unix(parseInt($('.event').attr('data-signup-opens'), 10));
        var secondsRemaining = signupTime.diff(moment(), 'seconds');
        if (secondsRemaining > 0) {
            var countdown = setInterval(function () {
                if (secondsRemaining <= 0) {
                    clearInterval(countdown);
                    history.go(0);
                } else if (secondsRemaining < 1800) {
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

})(jQuery, moment);
