function breakout_of_frame(){
    var request_data = document.location.search;
    var subpage = document.location.pathname.substr(18);
    var redirect_url = 'http://www.ntnuita.no';
    top.location.href = redirect_url + subpage + request_data;
}