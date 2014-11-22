/* globals blueimp */

(function ($, blueimp) {
    'use strict';

    // Make sure the data-description is added to the image
    $("#blueimp-gallery").on("slide", function (event, index) {
        var descr = $('[data-gallery]')[index].getAttribute('data-description'),
            node = $(blueimp.Gallery.prototype.options.container).find('.description');
        node.empty();
        if (descr) {
            node[0].appendChild(document.createTextNode(descr));
        }
    });
})(jQuery, blueimp);
