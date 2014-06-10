(function ($, slingsby) {
    "use strict";

    function setIcon(songId, imgPath) {
        $('#' + songId).attr('src', imgPath)
            .removeClass('clickable');
    }

    function vote(songId) {
        setIcon(songId, 'wait.gif');
        $.ajax({
            url: '/musikk/' + songId + '/vote/',
            type: 'POST',
            success: function () {
                setIcon(songId, slingsby.urls.musikk.successIcon);
            },
            error: function (jqXHR) {
                setIcon(songId, slingsby.urls.musikk.rejectIcon);
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
        /* jshint validthis:true */
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

    function init() {
        // Bind to the filter songs field
        $('input#song_filter').bind('keyup', filterSongList);

        // Bind to the vote button
        $(".song_vote_button").click(function () {
            var songId = $(this).attr('id');
            vote(songId);
        });

        // Display a loading symbol while loading audio
        $('audio').click(function () {
            if (this.readyState !== 4) {
                // Not loaded and ready to play, show waiting gif
                var $this = $(this);
                var $loadingImg = $this.siblings('.loading').find('img');
                $loadingImg.show();
                $this.on('playing', function () {
                    $loadingImg.hide();
                });
            }
        });

    }

    init();

})(jQuery, slingsby);
