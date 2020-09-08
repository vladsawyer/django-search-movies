$(function(){
  $('.minimized').click(function(event) {
    let i_path = $(this).attr('src');
    $('body').append('' +
        '<div id="overlay"></div>' +
        '<div id="magnify">' +
        '<img src="'+i_path+'">' +
        '<button type="button" id="close-popup" class="close" aria-label="Close">\n' +
        '  <span aria-hidden="true">&times;</span>\n' +
        '</button>' +
        '</div>');
    $('#magnify').css({
	    left: ($(document).width() - $('#magnify').outerWidth())/2,
        top: ($(window).height() - $('#magnify').outerHeight())/2
	  });
    $('#overlay, #magnify').fadeIn('fast');
  });

  $('body').on('click', '#close-popup, #overlay', function(event) {
    event.preventDefault();

    $('#overlay, #magnify').fadeOut('fast', function() {
      $('#close-popup, #magnify, #overlay').remove();
    });
  });
});