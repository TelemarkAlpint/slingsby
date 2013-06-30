{% load staticfiles %}

$(function(){
    $(".song_vote_button").click(function(){
        var song_id = $(this).attr('id');
        vote(song_id);
    })
});

function setIcon(song_id, img_path){
    $('#' + song_id).attr('src', '{% static "gfx/" %}' + img_path)
        .removeClass('clickable');
}

function vote(song_id){
    setIcon(song_id, 'wait.gif');
    $.ajax({
        url: '/musikk/' + song_id + '/vote/',
        type: 'POST',
        success: function(data, status, xhr){
            setIcon(song_id, 'check.png');
        },
        error: function(jqXHR, textStatus, errorThrown){
            setIcon(song_id, 'reject-16.png');
            alert(jqXHR.responseText);
        }
    });
}

function getHideFunc(htmlelement){
    if (jQuery(htmlelement).attr('data-slide') == 'true'){
        var hide = function(html){jQuery(html).slideUp()}
    } else {
        var hide = function(html){jQuery(html).hide()}
    }
    return hide;
}

function getShowFunc(htmlelement){
    if (jQuery(htmlelement).attr('data-slide') == 'true'){
        var show = function(html){jQuery(html).slideDown()}
    } else {
        var show = function(html){jQuery(html).show()}
    }
    return show;
}

function getSearchData(selector){
    if (jQuery(selector).attr("data-filter") !== undefined){
        var searchData = jQuery(selector).attr('data-filter').toLowerCase();
    } else {
        var searchData = jQuery(selector).html().toLowerCase();
    }
    return searchData;
}

function filterSongList(){
    var children = jQuery(this).attr('data-children');
    var searchText = jQuery(this).val().toLowerCase();
    var isEmpty = true;
    var show = getShowFunc(this);
    var hide = getHideFunc(this);
    jQuery(children).each(function(){
        var searchData = getSearchData(this);
        if (searchData.indexOf(searchText) != -1){
            show(this);
            isEmpty = false;
        } else {
            hide(this);
        }
    });
    if (isEmpty){
        show('#' + this.id + '_empty');
    } else {
        hide('#' + this.id + '_empty');
    }
}

$(function(){
    $('input#song_filter').bind('keyup', filterSongList);
});