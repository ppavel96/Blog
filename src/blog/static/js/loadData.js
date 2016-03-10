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

function loadPosts(inCategory) {
    if (loadPosts.nextID == undefined) {
        loadPosts.nextID = 0;
        loadPosts.noMore = false;
    }

    var LOAD_COUNT = 5;

    request = { navigation: 'posts', category: inCategory, id: loadPosts.nextID, count: LOAD_COUNT };
    callback = function (posts) {
        for (var i = 0; i < posts.length; i++) {
            var postClass = (i == 0 && loadPosts.nextID == 0) ? 'post' : 'post indent-needed';

            var text = '<div class="' + postClass + '">' +
                       '    <div class="content-inner">' +
                       '        <h3>' + posts[i].title + '</h3>' +
                       '        <p class="tiny">Опубликовал ' + posts[i].author + ' в ' + posts[i].blog + ' n минут назад</p>' +
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
    }

    if (!loadPosts.noMore)
        loadData(request, callback);
}
 