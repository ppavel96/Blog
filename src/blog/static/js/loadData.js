function loadData(request, callback) {
    if (loadData.isLoading == undefined)
        loadData.isLoading = false;

    var NEAR_BOTTOM_HEIGHT = 1000;

    if ($(window).scrollTop() + $(window).height() > $(document).height() - NEAR_BOTTOM_HEIGHT && !loadData.isLoading) {
        loadData.isLoading = true;

        $.ajax({
            dataType: "json",
            url: "/api/",
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
        loadPosts.startTime = new Date(Date.now());
    }

    var LOAD_COUNT = 5;

    var request = { method: 'posts.get', category: inCategory, id: loadPosts.nextID, count: LOAD_COUNT, older: loadPosts.startTime.toISOString() };
    if (!loadPosts.noMore)
        loadData(request, function (posts) {
            constructPosts(posts, true);

            loadPosts.nextID += posts.length;
            if (posts.length < LOAD_COUNT)
                loadPosts.noMore = true;
        });
}

function loadBlogs(inCategory) {
    if (loadBlogs.nextID == undefined) {
        loadBlogs.nextID = 0;
        loadBlogs.noMore = false;
        loadBlogs.startTime = new Date(Date.now());
    }

    var LOAD_COUNT = 10;

    var request = { method: 'blogs.get', category: inCategory, id: loadBlogs.nextID, count: LOAD_COUNT, older: loadBlogs.startTime.toISOString() };
    if (!loadBlogs.noMore)
        loadData(request, function (blogs) {
            constructBlogs(blogs);

            loadBlogs.nextID += blogs.length;
            if (blogs.length < LOAD_COUNT)
                loadBlogs.noMore = true;
        });
}

function loadPostByID(ID) {
    if (loadPostByID.OnlyOnce == undefined) {
        var request = { method: 'posts.getByID', id: ID };
        loadData(request, function (posts) {
            constructPosts(posts, false);
        });

        loadPostByID.OnlyOnce = true;
    }
}

function constructPosts(posts, bCommentLink) {
    for (var i = 0; i < posts.length; i++) {
        var postClass = (i == 0 && loadPosts.nextID == 0) ? 'post' : 'post indent-needed';
        var timerID = "postPublishTime_" + posts[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: Date.parse(posts[i].publishedDate)
        });

        var text = '<div class="' + postClass + '">' +
                    '    <div class="content-inner">' +
                    '        <h1><a href="/posts/' + posts[i].id + '/">' + posts[i].title + '</a></h1>' +
                    '        <p class="tiny">' +
                    '            <b>Автор:</b> ' + posts[i].author + '<b>; Блог:</b> ' + posts[i].blog + '; <b>Рейтинг:</b> ' + posts[i].rating + '; <b>Комментарии:</b> ' + posts[i].comments + '; <b>Опубликовано:</b> <span id="' + timerID + '"></span>' +
                    '        </p>' +
                    '        <br />';

        text += posts[i].HTMLContent;

        if (bCommentLink)
            text += '    <a class="content-right right-align-text" href="/posts/' + posts[i].id + '/">Читать комментарии... </a>';

        // THIS IS TEMPORARY
        else
            text += '    <br><h1 id="comments">Комментарии:</h1><p>Комментариев нет</p>'

        text += '    </div>' +
                    '</div>';

        $("#post_pool").append(text);
    }

    timersUpdate();
}

function constructBlogs(blogs) {
    for (var i = 0; i < blogs.length; i++) {
        var blogClass = (i == 0 && loadBlogs.nextID == 0) ? 'post' : 'post indent-needed';
        var timerID = "blogPublishTime_" + blogs[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: Date.parse(blogs[i].publishedDate)
        });

        var text = '<div class="' + blogClass + '">' +
                   '    <div class="table">' + 
                   '        <div class="table-cell content-inner">' +
                   '            <img src="' + blogs[i].avatar + '" alt="Blog avatar" width="120" height="120" />' +
                   '        </div>' +

                   '        <div class="table-cell content-inner">' +
                   '            <h1><a href="/blogs/' + blogs[i].id + '/">' + blogs[i].title + '</a></h1>' +
                   '            <p class="tiny">' +
                   '                <b>Участников:</b> ' + blogs[i].members + '<b>; Постов:</b> ' + blogs[i].posts + '; <b>Создан:</b> <span id="' + timerID + '"></span>' +
                   '            </p>' +
                   '            <br />' +

                   '            <p>' + blogs[i].description + '</p>' + 
                   '            <a class="content-right right-align-text" href="/blogs/' + blogs[i].id + '/">Читать посты... </a>' +
                   '        </div>' +
                   '    </div>' +
                   '</div>';

        $("#blog_pool").append(text);
    }

    timersUpdate();
}

timersToUpdate = [];
function timersUpdate() {
    for (var i = 0; i < timersToUpdate.length; i++) {
        var mins = Math.ceil((Date.now() - timersToUpdate[i].time) / 60000);

        if (mins > 60)
            $(timersToUpdate[i].id).text(Math.ceil(mins / 60).toString() + " часов(а) назад");
        else
            $(timersToUpdate[i].id).text(mins.toString() + " минут(ы) назад");
    }
}

setInterval(timersUpdate, 60000);
