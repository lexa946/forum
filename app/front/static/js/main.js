function createCommentCard(comment) {
    let nodeComment = '<div class="card my-3 comment" id="comment-{{ comment.id }}">' +
        '<div class="card-header">' + (comment.nick || 'Аноним') + ' | ' +
        moment(comment.create_at).format('HH:mm DD.MM.YYYY') +
        ' | №' + comment.id + " |" +
        '</div>' +
        '<div class="card-body">'

    if (comment.media.length > 0) {
        let arrPictures = []
        let arrVideos = []

        let pictureExtensions = ['jpg', 'jpeg', 'png', 'webp', 'tiff', 'gif']
        let videoExtensions = ['mp4', 'webm']


        for (let media of comment.media) {
            let extension = media.filename.split(".")[1]

            if (videoExtensions.includes(extension)) {
                arrVideos.push(media)
            } else if (pictureExtensions.includes(extension)) {
                arrPictures.push(media)
            }
        }
        console.log(arrVideos)
        console.log(arrPictures)

        nodeComment += '<div class="videos mb-2">'

        for (let video of arrVideos) {
            nodeComment += '<video id="my-player" class="m-2 video-js" data-setup="{}" controls width="320" height="240">'
            let videoType = ""
            console.log(video)
            if (video.filename.substr(-3) == "mp4") {
                videoType = "video/mp4"
            } else if (video.filename.substr(-4) == "webm") {
                videoType = "video/webm"
            }
            nodeComment += '<source src="' + video.s3_url + '#t=0.1" type="' + videoType + '">' +
                '</video>'
        }
        nodeComment += '</div>'


        nodeComment += '<div class="pictures mb-2">'
        for (let picture of arrPictures) {
            nodeComment += '<a href="' + picture.s3_url + '" data-lightbox="roadtrip" data-lightbox="' + picture.filename + '"' +
                '                           data-title="' + picture.filename + '">' +
                '                            <img src="' + picture.s3_url + '" class="img-thumbnail" alt="' + picture.filename + '"' +
                '                                 style="width: auto; max-height: 150px;">' +
                '                        </a>'
        }
        nodeComment += '</div>'

        nodeComment += '<div class="flex mb-5">'

        for (let media of comment.media) {
            console.log(media.s3_url)
            nodeComment += '<a class="btn btn-outline-primary" href="' + media.s3_url + '">' + media.filename + '</a>'
        }
        nodeComment += "</div>"
    }


    nodeComment += '<p class="card-text">' + comment.text + '</p>' +
        '<button class="btn">ответить</button>' +
        '</div>' +
        '</div>'


    return $(nodeComment)
};


// Обновление комментариев
$('#refresh').click(event => {

    let json = {
        thread_id: +$('form [name="thread_id"]').val(),
        offset: $('.comment').length,
    };

    $.ajax({

        url: "http://" + location.host + "/forum/api/v1/comment/thread",
        type: "GET",
        data: json,
    }).done(response => {
        console.log(response);

        response.comments.forEach(comment => {

            $('#comments').append(createCommentCard(comment));

        });

    });
});

//Добавление нового комментария
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
            let comment = response.comment;
            $('#comments').append(createCommentCard(comment));
            $('#text').val('');
        },
        error: function (jqXHR, exception) {
            alert('Проблема с добавлением комментария! Я хз че с тобой не так!');
        },
    });

});