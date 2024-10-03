$(function () {
    $('#add_comment').submit(function (e) {
        e.preventDefault();

        let form = $(this);
        let form_data = new FormData(form[0]);

        $.each(form.find('[name="files[]"]'), function (file) {
            form_data.append("files", $(this)[0].files[0])
        });

        $.ajax({
            url: "http://" + location.host + "/forum/api/v1/comment/",
            method: "POST",
            data: form_data,
            processData: false,
            contentType: false,
            success: function (response) {
                let nodeComment = '<div class="card my-3 comment" id="comment-{{ comment.id }}">' +
                    '<div class="card-header">' + (response.comment.nick || 'Аноним') + ' | ' +
                    moment(response.comment.create_at).format('HH:mm DD.MM.YYYY') +
                    ' | №' + response.comment.id + " |" +
                    '</div>' +
                    '<div class="card-body">'

                if(response.comment.media.length > 0){
                    nodeComment += "<div class=\"flex mb-5\">"

                    for (let media of response.comment.media) {
                        nodeComment += '<a class="btn btn-outline-primary"' +
                        '                           href="http://185.204.2.28:9000/forum/' + media.id +'_'+
                        media.filename + '">' + media.filename + '</a>'
                    }

                    nodeComment += "</div>"

                }

                nodeComment += '<p class="card-text">' + response.comment.text + '</p>' +
                    '<button class="btn">ответить</button>' +
                    '</div>' +
                    '</div>'


                let commentCard = $(nodeComment);
                $('#comments').append(commentCard);
                $('#text').val('');
            },
            error: function (jqXHR, exception) {
                alert('Проблема с добавлением комментария! Я хз че с тобой не так!');
            },
        });

    });
});

