(function(window, document, undefined){
    $("#suggest_quote").click(function () {
        $("#quote_suggestion").slideToggle(300);
        $(this).html(($(this).text() == "+") ? "-" : "+");
    });

    $('.quote_reject').submit(function(){
        var target = $(this).attr('action');
        $.ajax(target, {
            type: "POST",
            context: $(this),
            success: function(){
                var wrapper = $(this).parents('.suggested_quote_wrapper');
                wrapper.slideUp(function(){
                    wrapper.remove();
                });
            }
        });
        return false;
    });

    $('.quote_confirm').submit(function(){
        var target = $(this).attr('action');
        $.ajax(target, {
            type: "POST",
            context: $(this),
            success: function(){
                $('.suggested_quote_wrapper').slideUp(function(){
                    $(this).remove();
                });
            }
        });
        return false;
    });

    // Add click handling for the statusbar in the header
    $('#status .clickable').click(function(){
        var clickSymbol = '&#9660;'; // BLACK DOWN POINTING TRIANGLE
        if ($(this).hasClass('selected')){
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
})(this, document);