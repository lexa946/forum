function removeBtn(btn){
    console.log(btn.parentNode)
    console.log()
    $(btn.parentNode).remove();
}

$('#add_file').click(function (event) {

    let btnAddFile = $(this)
    let fileInput = $(
        '<div class="input-group mt-2">' +
        '  <input type="file" class="form-control" aria-describedby="inputGroupFileAddon04" aria-label="Upload" name="files[]">' +
        '  <button class="btn btn-outline-secondary" type="button" id="inputGroupFileAddon04" onclick="removeBtn(this)">-</button>' +
        '</div>'
    )
    btnAddFile.before(fileInput);
})