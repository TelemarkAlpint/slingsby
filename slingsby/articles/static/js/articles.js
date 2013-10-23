(function ($) {
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
    improveTimestamps();

    // Load disqus comment count for posts.
    (function () {
        var s = document.createElement('script');
        s.async = true;
        s.type = 'text/javascript';
        s.src = 'http://' + slingsby.config.DISQUS_IDENTIFIER + '.disqus.com/count.js';
        (document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());

    // Load more articles if approaching the end
    $(document).scroll(function () {

        var intBottomMargin = 500; //Pixels from bottom when script should trigger

        //if less than intBottomMargin px from bottom
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - intBottomMargin) {
            loadAjaxData();
        }

    });

    function loadAjaxData() {
        var loadingImage = $("#loadingImage");
        if (loadingImage.is(":hidden")) {
            loadingImage.show();
            var lastArticleDatetime = $('article:last').attr("data-datetime");
            var url = slingsby.urls.allArticles + "?limit=5&before=" + lastArticleDatetime;
            $.ajax(url, {
                dataType: "json",
                success: function (data) {
                    var html = slingsby.templates.articles(data);
                    $("#content").append(html);
                    improveTimestamps();
                },
                complete: function () {
                    loadingImage.hide();
                }
            });
        }
    }
})(jQuery);
