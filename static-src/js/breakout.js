(function breakoutOfFrame() {
    "use strict";

    var requestData = document.location.search;
    var subpage = document.location.pathname.substr(18);
    var redirectUrl = 'http://www.ntnuita.no';
    top.location.href = redirectUrl + subpage + requestData;
}());