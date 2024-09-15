
$('#refresh').click(event => {

        let json = {
            thread_id: +$('form [name="thread_id"]').val(),
            offset: $('.comment').length,
        };

        console.log(json);

        $.ajax({
//            url:"http://127.0.0.1:8082/forum/api/v1/comment/thread",
            url:"http://"+ location.host +"/forum/api/v1/comment/thread",
            type: "GET",
            data: json,
//            contentType: "application/json",
        }).done(response => {
            console.log(response);

            response.comments.forEach(comment => {
                let commentCard = $('<div class="card my-3 comment" id="comment-{{ comment.id }}">' +
                    '<div class="card-header">'+ (comment.nick || 'Аноним')+ ' | '+
                        moment(comment.create_at).format('HH:mm DD.MM.YYYY') +
                        ' | №' + comment.id +
                    '</div>'+
                    '<div class="card-body">' +
                        '<p class="card-text">'+ comment.text +'</p>'+
                        '<button class="btn">ответить</button>'+
                    '</div>'+
                '</div>');
                $('#comments').append(commentCard);

            });

        });
});
