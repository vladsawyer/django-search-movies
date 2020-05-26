(function($) {
  // defaults
  $.fn.fullClip = function(options) {
    const settings = $.extend({
      current: 0,
      images: [],
      transitionTime: 1000,
      wait: 3000,
      static: false
    }, options);

    // preload images
    let i, end;
    for (i = 0, end = settings.images.length; i < end; ++i) {
        new Image().src = settings.images[i];
    }

    // sort out the transitions + specify vendor prefixes
    $('.movie__bg-image').attr('src', settings.images[settings.current])

    // if only one image, set as static background
    if (settings.static) {
      $(this)
      .attr('src', settings.images[settings.current])
      return;
    }

    // change the image
    (function update() {
      settings.current = (settings.current + 1) % settings.images.length;
        $('.movie__bg-image').fadeOut(settings.transitionTime, function(){
          $(this).attr('src', settings.images[settings.current]).fadeIn(settings.transitionTime);
        });
        setTimeout(update, settings.wait);
    }());
}}(jQuery));
