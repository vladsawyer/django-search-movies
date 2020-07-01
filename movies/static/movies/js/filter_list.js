// variable that keeps all the filter information

let send_data = {};
$(document).ready(function () {
    // reset all parameters on page load

    resetFilters();
    // bring all the data without any filters


    // get all countries from database via

    // AJAX call into country select options

    getCountries();
    getGenres();
    getYears();
    getCategories();


    // on selecting the categories option

    $('#categories').on('change', function () {

        // update the selected categories

        if(this.value !== "all") {
            send_data['categories'] = this.value;
        }

        getAPIData();
    });

    // on filtering the years input

    $('#years').on('change', function () {
        // get the api data of updated years

        if(this.value !== "all"){
            send_data['years'] = this.value;
        }

        getAPIData();
    });

    // on filtering the genres input

    $('#genres').on('change', function () {
        // get the api data of updated years

        if(this.value !== "all"){
            send_data['genres'] = this.value;
        }
        getAPIData();
    });

    // on filtering the country input

    $('#countries').on('change', function () {
        if(this.value !== "all")
            send_data['countries'] = this.value;
        getAPIData();
    });

    // sort the data according to price/points

    $('#sort_by').on('change', function () {
        send_data['sort_by'] = this.value;
        getAPIData();
    });

    // display the results after reseting the filters

    $("#display_all").click(function(){
        resetFilters();
        getAPIData();
    })
})


/**
    Function that resets all the filters
**/
function resetFilters() {
    $("#categories").val("all");
    $("#years").val("all");
    $("#genres").val("all");
    $("#countries").val("all");
    $("#sort_by").val("none");

    send_data['categories'] = null;
    send_data['years'] = null;
    send_data['genres'] = null;
    send_data['countries'] = null;
    send_data['sort_by'] = null;
    send_data['format'] = 'json';

}

/**.
    Utility function to showcase the api data
    we got from backend to the  content
**/
function putData(result) {
    // creating table row for each result and

    // pushing to the html cntent of table body of listing table

    if (result["results"].length > 0){
        console.log(result["results"])
          $("#no_results").hide();
          let template = Hogan.compile(html);
          let output = template.render(result);
          const div = document.querySelector('.infinite-container');
          div.innerHTML = output;
    }


}

let html = `\
{{#results}}\
    <div class="col mb-4 infinite-item" >\
        <div class="card card-movie">\
            <div class="poster">\
                <img src="{{poster}}" alt="{{ title }}">\
            </div>\
    \
            <div class="rating">\
                <div class="imsp" title="IMDb">\
                    <i class="fab fa-imdb"></i>\
                    <label class="pl-1 m-0">{{ rating_imdb }}</label>\
                </div>\
    \
                <div class="kpsp" title="Kinopoisk">\
                    <span class="kp_sp"></span>\
                    <label class="m-0">{{ rating_kp }}</label>\
                </div>\
             </div>\
    \
            <div class="year text-white bg-success">\
                {{ year }}\
            </div>\
    \
            <div class="details">\
                <a href="{{ movie_url }}" class="title text-decoration-none"><h2>{{ title }}</h2></a>\
                {{#directors}}\
                <a href="{{member_url}}" class="director text-decoration-none"><span>{{full_name}}</span></a>\
                {{/directors}}\
                <div class="tags">\
                    {{#genres}}\
                        <a href="{{genre_url}}"><span class="badge badge-success">{{ title }}</span></a>\
                    {{/genres}}\
                </div>\
    \
                <div class="hover-derails p-0 m-0">\
                  <div class="info">\
                    {{if description}}\
                        <p>{{ description|truncatechars:180 }}</p>\
                    {{/if}}\
                  </div>\
    \
                  <div class="star">\
                  {{if actors}}\
                    <h4>Актеры</h4>\
                    <ul>\
                        {% for actor in actors.all %}\
                            <li><a href="{{actor.get_absolute_url}}" title="{{actor.full_name}}"><img src="{{ actor.image.url }}" alt=\"{{actor.full_name}}"></a></li>\
                        {% endfor %}\
                    </ul>\
                  {{/if}}\
                  </div>\
                </div>\
            </div>\
        </div>\
    </div>\
{{/results}}`

function getAPIData() {
    let url = $('#movie_list').attr("url")
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            putData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#movie_list").hide();
        }
    });
}


function getCountries() {
    // fill the options of countries by making ajax call

    // obtain the url from the countries select input attribute

    let url = $("#countries").attr("url");

    // makes request to get_countries(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            let countries_option = "<option value='all' selected>Все страны</option>";
            $.each(result["countries"], function (a, b) {
                countries_option += "<option>" + b + "</option>"
            });
            $("#countries").html(countries_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getGenres() {
    // fill the options of genres by making ajax call

    // obtain the url from the genres select input attribute

    let url = $("#genres").attr("url");

    // makes request to get_genres(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            let genres_option = "<option value='all' selected>Все жанры</option>";
            $.each(result["genres"], function (a, b) {
                genres_option += `<option value='${b["slug"]}'>${b["title"]}</option>`
            });
            $("#genres").html(genres_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getYears() {
    // fill the options of years by making ajax call

    // obtain the url from the years select input attribute

    let url = $("#years").attr("url");

    // makes request to get_years(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            let years_option = "<option value='all' selected>Все года</option>";
            $.each(result["years"], function (a, b) {
                years_option += "<option>" + b + "</option>"
            });
            $("#years").html(years_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getCategories() {
    // fill the options of categories by making ajax call

    // obtain the url from the categories select input attribute

    let url = $("#categories").attr("url");

    // makes request to get_categories(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            let categories_option = "<option value='all' selected>Что ищем</option>";
            $.each(result["categories"], function (a, b) {
                categories_option += `<option value='${b["slug"]}'>${b["title"]}</option>`
            });
            $("#categories").html(categories_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

