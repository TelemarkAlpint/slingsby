(function ($) {
    "use strict";

    $("#suggest_quote").click(function () {
        $("#quote_suggestion").slideToggle(300);
        $(this).html(($(this).text() === "+") ? "-" : "+");
    });

    $('.quote_reject').submit(function () {
        var target = $(this).attr('action');
        $.ajax(target, {
            type: "DELETE",
            context: $(this),
            success: function () {
                var wrapper = $(this).parents('.suggested_quote_wrapper');
                wrapper.slideUp(function () {
                    wrapper.remove();
                });
            }
        });
        return false;
    });

    $('.quote_confirm').submit(function () {
        var target = $(this).attr('action');
        $.ajax(target, {
            type: "POST",
            context: $(this),
            success: function () {
                $('.suggested_quote_wrapper').slideUp(function () {
                    $(this).remove();
                });
            }
        });
        return false;
    });

    // Add click handling for the statusbar in the header
    $('#status .clickable').click(function () {
        var clickSymbol = '&#9660;'; // BLACK DOWN POINTING TRIANGLE
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            clickSymbol =  '&#9664;'; // BLACK LEFT POINTING TRIANGLE
            $(this).parent().find('ul').slideUp();
            $(this).find('.click_symbol').removeClass('rotated_left');
        } else {
            $(this).addClass('selected');
            $(this).parent().find('ul').slideDown();
            $(this).find('.click_symbol').addClass('rotated_left');
        }
        //$(this).find('.click_symbol').html(clickSymbol);
    });

    /*
     * Because facebook screws up as usual.
     * Creds to PapaSierra: http://stackoverflow.com/questions/7131909/facebook-callback-appends-to-return-url
     */
    function cleanUpHFacebookHash() {
        if (window.location.hash === '#_=_') {

            // Check if the browser supports history.replaceState.
            if (history.replaceState) {

                // Keep the exact URL up to the hash.
                var cleanHref = window.location.href.split('#')[0];

                // Replace the URL in the address bar without messing with the back button.
                history.replaceState(null, null, cleanHref);

            } else {

                // Well, you're on an old browser, we can get rid of the _=_ but not the #.
                window.location.hash = '';
            }
        }
    }

    $(document).ready(function () {
        cleanUpHFacebookHash();
    });

})(jQuery);
