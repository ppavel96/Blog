function loadGeneric(url, request, callback) {
    if (loadGeneric.isLoading == undefined) {
        loadGeneric.isLoading = false;
        loadGeneric.startTime = (new Date(Date.now())).toISOString();

        loadGeneric.noMore = {}
        loadGeneric.nextID = {}
        loadGeneric.loaded = {}

        loadGeneric.NEAR_BOTTOM_HEIGHT = 1000;
    }

    if (!loadGeneric.nextID.hasOwnProperty(url)) {
        loadGeneric.nextID[url] = 0;
        loadGeneric.loaded[url] = {}
    }

    if (loadGeneric.noMore.hasOwnProperty(url))
        return;

    request['count'] = 20;
    request['id'] = loadGeneric.nextID[url];
    request['older'] = loadGeneric.startTime;

    if ($(window).scrollTop() + $(window).height() > $(document).height() - loadGeneric.NEAR_BOTTOM_HEIGHT && !loadGeneric.isLoading) {
        loadGeneric.isLoading = true;

        $.ajax({
            dataType: "json",
            url: url,
            data: request,
            success: function(data) {
                loadGeneric.nextID[url] += data.length;
                if (data.length < request.count)
                    loadGeneric.noMore = true;

                newdata = []
                for (i = 0; i < data.length; i++) {
                    if (!loadGeneric.loaded[url].hasOwnProperty(data[i].id)) {
                        loadGeneric.loaded[url][data[i].id] = true;
                        newdata.push(data[i]);
                    }
                }

                callback(newdata);
            },

            complete: function () { loadGeneric.isLoading = false; }
        });
    }
}

function loadPosts(inCategory) {
    loadGeneric('/api/posts.get', { category: inCategory }, constructPosts);
}

function loadBlogs(inCategory) {
    loadGeneric('/api/blogs.get', { category: inCategory }, constructBlogs);
}

function constructPosts(posts) {
    for (var i = 0; i < posts.length; i++) {
        var timerID = "postPublishTime_" + posts[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: Date.parse(posts[i].publishedDate)
        });

        var text = '<div class="post indent-needed">' +
                    '    <div class="content-inner">' +
                    '        <h1><a href="/posts/' + posts[i].id + '/">' + posts[i].title + '</a></h1>' +
                    '        <p class="tiny">' +
                    '            <b>Автор:</b> ' + posts[i].author + '<b>; Блог:</b> ' + posts[i].blog + '; <b>Рейтинг:</b> ' + posts[i].cachedRating + '; <b>Комментарии:</b> ' + posts[i].cachedCommentsNumber + '; <b>Опубликовано:</b> <span id="' + timerID + '"></span>' +
                    '        </p>' +
                    '        <br />';

        text += posts[i].content;

        text +=     '    <a class="content-right right-align-text" href="/posts/' + posts[i].id + '/">Читать комментарии... </a>' + 
                    '    </div>' +
                    '</div>';

        $("#post_pool").append(text);
    }

    timersUpdate();
}

function constructBlogs(blogs) {
    for (var i = 0; i < blogs.length; i++) {
        var timerID = "blogPublishTime_" + blogs[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: Date.parse(blogs[i].publishedDate)
        });

        var text = '<div class="post indent-needed">' +
                   '    <div class="table">' + 
                   '        <div class="table-cell content-inner">' +
                   '            <img src="' + blogs[i].image + '" alt="Blog avatar" width="120" height="120" />' +
                   '        </div>' +

                   '        <div class="table-cell content-inner">' +
                   '            <h1><a href="/blogs/' + blogs[i].id + '/">' + blogs[i].title + '</a></h1>' +
                   '            <p class="tiny">' +
                   '                <b>Участников:</b> ' + blogs[i].cachedMembersNumber + '<b>; Постов:</b> ' + blogs[i].cachedPostsNumber + '; <b>Создан:</b> <span id="' + timerID + '"></span>' +
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
