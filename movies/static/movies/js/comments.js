function addComment(name, id) {
        document.getElementById("comment-parent").value = id;
        document.getElementById("contact-comment").innerText = `${name}, `
    }


$("#comments").on("click", "#likebutton", function(){
    let comment_id;
    let user_id;
    let url;
    comment_id = $(this).attr("data-catid");
    user_id = $('#form-comment > input[name$="user"]').attr('value');
    url = $(this).attr('data-url');

    $.ajax(
    {
        type:"GET",
        url: url,
        data:{
            comment_id: comment_id,
            user_id: user_id,
            },
        success: function( data )
        {
            $( '#like'+ comment_id ).removeClass('far fa-heart fa-fw fa-lg');
            $( '#like'+ comment_id ).addClass('fas fa-heart fa-fw fa-lg');
            $( '#like'+ comment_id ).style = 'color: #ffc107';
            $('#total_likes' + comment_id).text(data['total_likes']);
        },
        success_dislike: function( data )
        {
            $( '#like'+ comment_id ).removeClass('fas fa-heart fa-fw fa-lg');
            $( '#like'+ comment_id ).addClass('far fa-heart fa-fw fa-lg');
            $( '#like'+ comment_id ).style = 'color: #fff';
        },
    })
});