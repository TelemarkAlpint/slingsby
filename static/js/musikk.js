$(function(){
    $(".song_vote_button").click(function(){
	var song_id = $(this).attr('id');
	vote(song_id);
    })
});

function set_icon(song_id, img_path){
    $('#' + song_id).attr('src', '{{ GRAPHICS_DIR }}' + img_path)
	.removeClass('clickable');
}

function vote(song_id){
    set_icon(song_id, 'wait.gif');
    $.ajax({
	url: '/musikk/' + song_id + '/vote/',
	type: 'POST',
	data: {
	    id: song_id,
	},
	success: function(data, status, xhr){
	    set_icon(song_id, 'check.png');
	},
	error: function(jqXHR, textStatus, errorThrown){
	    set_icon(song_id, 'reject-16.png');
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

function filter_list(){
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
    $('input#song_filter').bind('keyup', filter_list);
});