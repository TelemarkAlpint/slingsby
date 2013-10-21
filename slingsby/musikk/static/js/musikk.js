(function ($) {
    "use strict";

    function setIcon(songId, imgPath) {
        $('#' + songId).attr('src', slingsby.urls.GRAPHICS_URL + imgPath)
            .removeClass('clickable');
    }

    function vote(songId) {
        setIcon(songId, 'wait.gif');
        $.ajax({
            url: '/musikk/' + songId + '/vote/',
            type: 'POST',
            success: function () {
                setIcon(songId, 'check.png');
            },
            error: function (jqXHR) {
                setIcon(songId, 'reject-16.png');
                alert(jqXHR.responseText);
            }
        });
    }

    function getHideFunc(htmlelement) {
        var hide;
        if (jQuery(htmlelement).attr('data-slide') === 'true') {
            hide = function (html) {jQuery(html).slideUp(); };
        } else {
            hide = function (html) {jQuery(html).hide(); };
        }
        return hide;
    }

    function getShowFunc(htmlelement) {
        var show;
        if (jQuery(htmlelement).attr('data-slide') === 'true') {
            show = function (html) {jQuery(html).slideDown(); };
        } else {
            show = function (html) {jQuery(html).show(); };
        }
        return show;
    }

    function getSearchData(selector) {
        var searchData;
        if (jQuery(selector).attr("data-filter") !== undefined) {
            searchData = jQuery(selector).attr('data-filter').toLowerCase();
        } else {
            searchData = jQuery(selector).html().toLowerCase();
        }
        return searchData;
    }

    function filterSongList() {
        var children = jQuery(this).attr('data-children');
        var searchText = jQuery(this).val().toLowerCase();
        var isEmpty = true;
        var show = getShowFunc(this);
        var hide = getHideFunc(this);
        jQuery(children).each(function () {
            var searchData = getSearchData(this);
            if (searchData.indexOf(searchText) !== -1) {
                show(this);
                isEmpty = false;
            } else {
                hide(this);
            }
        });
        if (isEmpty) {
            show('#' + this.id + '_empty');
        } else {
            hide('#' + this.id + '_empty');
        }
    }

    /* Stuff to be done onload, assign listeners etc */
    $(document).ready(function () {
        $('input#song_filter').bind('keyup', filterSongList);

        $(".song_vote_button").click(function () {
            var songId = $(this).attr('id');
            vote(songId);
        });
    });
})(jQuery);
