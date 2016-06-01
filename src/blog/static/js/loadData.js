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

    request['count'] = 5;
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

function constructPosts(posts, comment_link = true) {
    for (var i = 0; i < posts.length; i++) {
        var timerID = "postPublishTime_" + posts[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: new Date(posts[i].publishedDate)
        });

        var text =  '<div>' +
                    '    <div class="content-inner">' +
                    '        <h1><a href="/posts/' + posts[i].id + '/">' + posts[i].title + '</a></h1>' +
                    '        <p class="tiny">' +
                    '            <b class="interest0">Author:</b> ' + posts[i].author + '; <b class="interest1">Blog:</b> ' + posts[i].blog + '; <b class="interest2">Rating:</b> ' + posts[i].cachedRating + '; <b class="interest3">Comments:</b> ' + posts[i].cachedCommentsNumber + '; <b class="interest4">Followed by:</b> ' + posts[i].cachedSubscriptionsNumber + '; <b class="interest5">Published:</b> <span id="' + timerID + '"></span>' + '<br>' +
                    '            <b class="interest0">Tags:</b> ';

        for (var j = 0; j < posts[i].tags.length; ++j)
            text += posts[i].tags[j] + '; ';

        text +=     '        </p>' +
                    '        <br />';

        text += posts[i].content;

        if (comment_link)
            text += '    <br>' +
                    '    <a href="/posts/' + posts[i].id + '/">Go to comments... </a>';

        text +=     '    </div>' +
                    '</div>' +
                    '<hr><br>';

        if (!comment_link)
            text += '<div><div class="content-inner" id="comment_pool"><h1>Comments</h1></div></div>';

        $("#post_pool").append(text);
    }

    timersUpdate();
}

function constructBlogs(blogs) {
    for (var i = 0; i < blogs.length; i++) {
        var timerID = "blogPublishTime_" + blogs[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: new Date(blogs[i].publishedDate)
        });

        var text = '<div>' +
                   '    <div class="table">' + 
                   '        <div class="table-cell content-inner">' +
                   '            <img src="' + blogs[i].image + '" alt="Blog avatar" width="120" height="120" />' +
                   '        </div>' +

                   '        <div class="table-cell content-inner">' +
                   '            <h1><a href="/blogs/' + blogs[i].id + '/">' + blogs[i].title + '</a></h1>' +
                   '            <p class="tiny">' +
                   '                <b class="interest0">Moderator: </b> ' + blogs[i].creator + '; <b class="interest1">Members:</b> ' + blogs[i].cachedMembersNumber  + '; <b class="interest2">Rating:</b> ' + blogs[i].cachedBlogRating + '; <b class="interest3">; Posts:</b> ' + blogs[i].cachedPostsNumber + '; <b  class="interest4">Created:</b> <span id="' + timerID + '"></span>' +
                   '            </p>' +
                   '            <br />' +

                   '            <p>' + blogs[i].description + '</p>' + '<br />' + 
                   '            <a href="/blogs/' + blogs[i].id + '/">Go to posts... </a>' +
                   '        </div>' +
                   '    </div>' +
                   '</div>' +
                   '<br><hr><br>';

        $("#blog_pool").append(text);
    }

    timersUpdate();
}

timersToUpdate = [];
function timersUpdate() {
    for (var i = 0; i < timersToUpdate.length; i++) {
        var mins = Math.floor((Date.now() - timersToUpdate[i].time) / 60000);

        if (mins >= 2880) {
            $(timersToUpdate[i].id).text(Math.ceil(mins / 1440).toString() + " days ago");
            continue;
        }

        if (mins >= 1440) {
            $(timersToUpdate[i].id).text(Math.ceil(mins / 1440).toString() + " day ago");
            continue;
        }

        if (mins >= 120) {
            $(timersToUpdate[i].id).text(Math.ceil(mins / 60).toString() + " hours ago");
            continue;
        }

        if (mins > 60) {
            $(timersToUpdate[i].id).text(Math.ceil(mins / 60).toString() + " hour ago");
            continue;
        }

        if (mins > 1) {
            $(timersToUpdate[i].id).text(mins.toString() + " minutes ago");
            continue;
        }

        if (mins == 1) {
            $(timersToUpdate[i].id).text(mins.toString() + " minute ago");
            continue;
        }

        $(timersToUpdate[i].id).text("less than a minute ago");
    }
}

setInterval(timersUpdate, 60000);
