function loadData(request, callback) {
    if (loadData.isLoading == undefined)
        loadData.isLoading = false;

    var NEAR_BOTTOM_HEIGHT = 300;

    if ($(window).scrollTop() + $(window).height() > $(document).height() - NEAR_BOTTOM_HEIGHT && !loadData.isLoading) {
        loadData.isLoading = true;

        $.ajax({
            dataType: "json",
            url: "/ajax/",
            data: request,
            success: callback,
            complete: function () { loadData.isLoading = false; }
        });
    }
}

timersToUpdate = [];
function timersUpdate() {
    for (var i = 0; i < timersToUpdate.length; i++) {
        var mins = Math.ceil((Date.now() - timersToUpdate[i].time) / 60000);
        $('#' + timersToUpdate[i].id).text(mins.toString());
    }
}

setInterval(timersUpdate, 60000);

function loadPosts(inCategory) {
    if (loadPosts.nextID == undefined) {
        loadPosts.nextID = 0;
        loadPosts.noMore = false;
    }

    var LOAD_COUNT = 5;

    var request = { navigation: 'posts', category: inCategory, id: loadPosts.nextID, count: LOAD_COUNT };
    var callback = function (posts) {
        for (var i = 0; i < posts.length; i++) {
            var postClass = (i == 0 && loadPosts.nextID == 0) ? 'post' : 'post indent-needed';
            timersToUpdate.push({
                id: "publishTime_" + (loadPosts.nextID + i).toString(),
                time: Date.parse(posts[i].publishedDate)
            });

            var text = '<div class="' + postClass + '">' +
                       '    <div class="content-inner">' +
                       '        <h3>' + posts[i].title + '</h3>' +
                       '        <p class="tiny">Опубликовал ' + posts[i].author + ' в ' + posts[i].blog + ' <span id="' + timersToUpdate[timersToUpdate.length - 1].id + '"></span>' + ' минут назад</p>' +
                       '        <br />';

            text += posts[i].HTMLContent;

            text +=    '    <a class="content-right right-align-text" href="/posts/1/">Читать комментарии... </a>' +
                       '    </div>' +
                       '</div>';

            $("#post_pool").append(text);
        }

        loadPosts.nextID += posts.length;
        if (posts.length < LOAD_COUNT)
            loadPosts.noMore = true;

        timersUpdate();
    }

    if (!loadPosts.noMore)
        loadData(request, callback);
}
