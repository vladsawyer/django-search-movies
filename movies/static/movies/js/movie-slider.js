$('.center').slick({
    arrows: false,
    centerMode: true,
    infinite: true,
    autoplay: true,
    centerPadding: '60px',
    speed: 500,
    variableWidth: true,
});

$('.slider-movies').slick({
    infinite: false,
    speed: 300,
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 4,
                slidesToScroll: 4,
                infinite: true,
                dots: true
            }
            },
        {
            breakpoint: 830,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3
            }
            },
        {
            breakpoint: 600,
            settings: {
                arrows: false,
                slidesToShow: 2,
                slidesToScroll: 2
            }
            },
        {
            breakpoint: 480,
            settings: {
                arrows: false,
                slidesToShow: 2,
                slidesToScroll: 2
            }
        }]
});

$('.slider-collections').slick({
    infinite: false,
    speed: 300,
    slidesToShow: 3,
    slidesToScroll: 3,
    responsive: [
        {
            breakpoint: 1024,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 3,
                infinite: true,
                dots: true
            }
        },
        {
            breakpoint: 830,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2
            }
            },
        {
            breakpoint: 600,
            settings: {
                arrows: false,
                slidesToShow: 2,
                slidesToScroll: 2
            }
        },
        {
            breakpoint: 480,
            settings: {
                arrows: false,
                slidesToShow: 1,
                slidesToScroll: 1
            }
        }]
});