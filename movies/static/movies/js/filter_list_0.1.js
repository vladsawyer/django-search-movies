let send_data = {};
$(document).ready(function () {

    getCountries();
    getGenres();
    getYears();
    getCategories();


    $("#display_all").click(function(){
        resetFilters();
    })
})

function sel_categories() {
    $("#categories").val(`${getUrlVars()['categories']}`);
}


function getUrlVars() {
    let vars = {};
    let parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

/**
    Function that resets all the filters
**/
function resetFilters() {
    $("#categories").val("");
    $("#years").val("");
    $("#genres").val("");
    $("#countries").val("");
    $("#sort_by").val("");

    // send_data['categories'] = null;
    // send_data['years'] = null;
    // send_data['genres'] = null;
    // send_data['countries'] = null;
    // send_data['sort_by'] = null;
    // send_data['format'] = 'json';

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

            let countries_option = "<option value='' selected>Все страны</option>";
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

            let genres_option = "<option value='' selected>Все жанры</option>";
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

            let years_option = "<option value='' selected>Все года</option>";
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

            let categories_option = "<option value='' selected>Что ищем</option>";
            $.each(result["categories"], function (a, b) {
                categories_option += `<option id='${b["slug"]}' value='${b["slug"]}'>${b["title"]}</option>`
            });
            $("#categories").html(categories_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}