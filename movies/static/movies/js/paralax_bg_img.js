$(window).scroll(function(e){
  parallax();
});

function parallax(){
  let scrolled = $(window).scrollTop();
  $('.movie__bg-image').css('transform', 'translate3d(0px,' + (scrolled*0.025) + '%, 0px)');
}