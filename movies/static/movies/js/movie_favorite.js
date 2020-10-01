function addFavorite()
{
    let favorite = $("#favorite_button");
    let url = favorite.data('url');
    let csrf = favorite.data('csrf_token');

    $.ajax({
        url : url,
        type : 'POST',
        data : {
            'csrfmiddlewaretoken': csrf
        },

        success : function (response) {
              $(".favorites>button>i").removeClass("far");
            $(".favorites>button>i").addClass("fas");
            document.getElementById("favorite_button").style.color = "#ffc107";
            document.getElementById("favorite_button").title = "Убрать из избранного";
            $("#favorite_button").attr("data-action", "remove-favorite").data("data-action", "remove-favorite");
        }
    });

    return false;
}

function removeFavorite()
{
    let favorite = $("#favorite_button");
    let url = favorite.data('url');
    let csrf = favorite.data('csrf_token');
        console.log(url)
    console.log(csrf)
    console.log(favorite)

    $.ajax({
        url : url,
        type : 'POST',
        data : {
            'csrfmiddlewaretoken': csrf
        },

        success : function (response) {
            $(".favorites>button>i").removeClass("fas");
            $(".favorites>button>i").addClass("far");
            document.getElementById("favorite_button").style.color = "#fff";
            document.getElementById("favorite_button").title = "Добавить в избранного";
            $("#favorite_button").attr('data-action', "add-favorite").data('data-action', "add-favorite");
        }
    });

    return false;
}

// Подключение обработчиков

$('#favorite_button').click(function() {
    let action = $(this).attr('data-action');

    if (action === "add-favorite") {
        console.log(true)
        addFavorite()
    }
    else if(action === "remove-favorite"){
        console.log(false)
        removeFavorite()
    }
});
