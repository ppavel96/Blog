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
        loadPosts.startTime = new Date(Date.now());
    }

    var LOAD_COUNT = 5;

    var request = { navigation: 'posts', category: inCategory, id: loadPosts.nextID, count: LOAD_COUNT, older: loadPosts.startTime.toISOString() };
    if (!loadPosts.noMore)
        loadData(request, function (posts) {
            constructPosts(posts);

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

    var request = { navigation: 'blogs', category: inCategory, id: loadBlogs.nextID, count: LOAD_COUNT, older: loadBlogs.startTime.toISOString() };
    if (!loadBlogs.noMore)
        loadData(request, function (blogs) {
            constructBlogs(blogs);

            loadBlogs.nextID += blogs.length;
            if (blogs.length < LOAD_COUNT)
                loadBlogs.noMore = true;
        });
}

function constructPosts(posts) {
    for (var i = 0; i < posts.length; i++) {
        var postClass = (i == 0 && loadPosts.nextID == 0) ? 'post' : 'post indent-needed';

        timersToUpdate.push({
            id: "publishTime_" + (loadPosts.nextID + i).toString(),
            time: Date.parse(posts[i].publishedDate)
        });

        var text = '<div class="' + postClass + '">' +
                   '    <div class="content-inner">' +
                   '        <h3>' + posts[i].title + '</h3>' +
                   '        <p class="tiny">Опубликовал ' + posts[i].author + ' в ' + posts[i].blog + ' <span id="' + timersToUpdate[timersToUpdate.length - 1].id + '"></span></p>' +
                   '        <br />';

        text += posts[i].HTMLContent;

        text +=    '    <a class="content-right right-align-text" href="/posts/1/">Читать комментарии... </a>' +
                   '    </div>' +
                   '</div>';

        $("#post_pool").append(text);
    }

    timersUpdate();
}

function constructBlogs(blogs) {
    for (var i = 0; i < blogs.length; i++) {
        var blogClass = (i == 0 && loadBlogs.nextID == 0) ? 'post' : 'post indent-needed';

        var text = '<div class="' + blogClass + '">' +
                   '    <div class="table">' + 
                   '        <div class="table-cell content-inner">' +
                   '            <img src="' + blogs[i].avatar + '" alt="Blog avatar" width="100" height="100" />' +
                   '        </div>' +

                   '        <div class="table-cell content-inner">' +
                   '            <h3>' + blogs[i].title + '</h3>' +
                   '            <p>' + blogs[i].description + '</p>' + 
                   '            <a class="content-right right-align-text" href="/blogs/1/">Читать посты... </a>' +
                   '        </div>' +
                   '    </div>' +
                   '</div>';

        $("#blog_pool").append(text);
    }
}

timersToUpdate = [];
function timersUpdate() {
    for (var i = 0; i < timersToUpdate.length; i++) {
        var mins = Math.ceil((Date.now() - timersToUpdate[i].time) / 60000);
        if (mins > 60) {
            var hours = Math.ceil(mins / 60);
            $('#' + timersToUpdate[i].id).text(hours.toString() + " часов(а) назад");
        } else
            $('#' + timersToUpdate[i].id).text(mins.toString() + " минут(ы) назад");
    }
}

setInterval(timersUpdate, 60000);
