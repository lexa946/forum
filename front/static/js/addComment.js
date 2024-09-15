$(function() {
      $('#add_comment').submit(function(e) {
            let $form = $(this);

            let json = {
                thread_id: +$form.find('[name="thread_id"]').val(),
                nick: $form.find('[name="nick"]').val(),
                text: $form.find('[name="text"]').val(),
            }

            console.log(json);
            console.log(JSON.stringify(json));

            $.ajax({
//                  url: "http://127.0.0.1:8082/forum/api/v1/comment/",
                  url: "http://"+location.host+"/forum/api/v1/comment/",
                  type: "POST",
                  data: JSON.stringify(json),
                  contentType: "application/json",
            }).done(function(response ) {
                let commentCard = $('<div class="card my-3 comment" id="comment-{{ comment.id }}">' +
                    '<div class="card-header">'+ (response.comment.nick || 'Аноним')+ ' | '+
                        moment(response.comment.create_at).format('HH:mm DD.MM.YYYY') +
                        ' | №' + response.comment.id +
                    '</div>'+
                    '<div class="card-body">' +
                        '<p class="card-text">'+ response.comment.text +'</p>'+
                        '<button class="btn">ответить</button>'+
                    '</div>'+
                '</div>');
                $('#comments').append(commentCard);
                $('#text').val('');


            }).fail(function() {
                alert('Проблема с добавлением комментария! Я хз че с тобой не так!');
            });
            //отмена действия по умолчанию для кнопки submit
            e.preventDefault();
      });
});