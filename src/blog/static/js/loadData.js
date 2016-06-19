"use strict";
function loadGeneric(url, request, callback) {
    if (loadGeneric.isLoading == undefined) {
        loadGeneric.isLoading = false;
        loadGeneric.startTime = new Date(Date.now()).toISOString();

        loadGeneric.noMore = {};
        loadGeneric.nextID = {};
        loadGeneric.loaded = {};

        loadGeneric.NEAR_BOTTOM_HEIGHT = 1000;
    }

    if (!loadGeneric.nextID.hasOwnProperty(url)) {
        loadGeneric.nextID[url] = 0;
        loadGeneric.loaded[url] = {};
    }

    if (loadGeneric.noMore.hasOwnProperty(url)) {
        return;
    }

    request.id = loadGeneric.nextID[url];
    request.older = loadGeneric.startTime;

    if ((loadGeneric.nextID[url] == 0 || $(document).scrollTop() + $(window).height() > $(document).height() - loadGeneric.NEAR_BOTTOM_HEIGHT) && !loadGeneric.isLoading) {
        loadGeneric.isLoading = true;

        $.ajax({
            dataType: "json",
            url: url,
            data: request,
            success: function (data) {
                loadGeneric.nextID[url] += data.length;
                if (data.length < request.count) {
                    loadGeneric.noMore = true;
                }

                var newdata = [];
                for (var i = 0; i < data.length; i += 1) {
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
    loadGeneric('/api/posts.get', { category: inCategory, count: 5 }, constructPosts);
}

function loadBlogs(inCategory) {
    loadGeneric('/api/blogs.get', { category: inCategory, count: 5 }, constructBlogs);
}

function loadUsers() {
    loadGeneric('/api/users.get', { count: 20 }, constructUsers);
}

function loadFollowers(user_id) {
    loadGeneric('/api/users.getFollowers', { count: 20, user_id: user_id }, constructUsers);
}

function loadSubscriptions(user_id) {
    loadGeneric('/api/users.getSubscriptionsForUsers', { count: 20, user_id: user_id }, constructUsers);
}

function loadSubscriptionsForPosts(user_id) {
    loadGeneric('/api/users.getSubscriptionsForPosts', { count: 20, user_id: user_id }, constructPosts);
}

function constructPosts(posts, comment_link) {
    comment_link = typeof comment_link != 'undefined' ? comment_link : true;

    for (var i = 0; i < posts.length; i += 1) {
        var timerID = "postPublishTime_" + posts[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: new Date(posts[i].publishedDate)
        });

        var fav_data = posts[i].is_subscribed;
        var fav_icon = fav_data == 1 ? '/static/favorite_pressed.png' : '/static/favorite.png';

        var vote_data = posts[i].vote;
        var upvote_icon = vote_data == 1 ? '/static/upvote_pressed.png' : '/static/upvote.png';
        var downvote_icon = vote_data == -1 ? '/static/downvote_pressed.png' : '/static/downvote.png';

        var text =  '<div>' +
                    '    <div class="content-inner">' +
                    '        <table><td><input class="vote" type="image" src="' + upvote_icon + '" alt="up" data-vote="' + vote_data + '" onclick="voteForPost(this, \'up\', ' + posts[i].id + ')" /><input class="vote" type="image" src="' + downvote_icon + '" alt="down" data-vote="' + vote_data + '" onclick="voteForPost(this, \'down\', ' + posts[i].id + ')" /></td>' +
                    '        <td><input class="vote" type="image" src="' + fav_icon + '" alt="fav" data-fav="' + fav_data + '" onclick="subscribeForPost(this, ' + posts[i].id + ')" /></td>' +
                    '        <td><h1><a target="_blank" href="/posts/' + posts[i].id + '/">' + posts[i].title + '</a></h1></td></table>' +
                    '        <p class="tiny">' +
                    '            <b class="interest0">Author:</b> <a class="usual" target="_blank" href="/profile/' + posts[i].author_id + '/">' + posts[i].author + '</a>; <b class="interest1">Blog:</b> <a class="usual" target="_blank" href="/blogs/' + posts[i].blog_id + '/">' + posts[i].blog + '</a>; <b class="interest2">Rating:</b> <span id="post-rating' + posts[i].id + '">' + posts[i].cachedRating + '</span>; <b class="interest3">Comments:</b> ' + posts[i].cachedCommentsNumber + '; <b class="interest4">Followed by:</b> <span id="post-followers' + posts[i].id + '">' + posts[i].cachedPostFollowersNumber + '</span>; <b class="interest5">Published:</b> <span id="' + timerID + '"></span>' + '<br>' +
                    '            <b class="interest0">Tags:</b> ';

        for (var j = 0; j < posts[i].tags.length; j += 1)
            text += '<a class="usual" target="_blank" href="/tags/' + posts[i].tags[j] + '/">' + posts[i].tags[j] + '</a>; ';

        text +=     '        </p>' +
                    '        <br />';

        text += posts[i].content;

        if (comment_link)
            text += '    <br>' +
                    '    <a target="_blank" href="/posts/' + posts[i].id + '/">Go to comments... </a>';

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
    for (var i = 0; i < blogs.length; i += 1) {
        var timerID = "blogPublishTime_" + blogs[i].id;

        timersToUpdate.push({
            id: "#" + timerID,
            time: new Date(blogs[i].publishedDate)
        });

        var fav_data = blogs[i].is_subscribed;
        var fav_icon = fav_data == 1 ? '/static/favorite_pressed.png' : '/static/favorite.png';

        var text = '<div>' +
                   '    <div class="table">' +
                   '        <div class="table-cell content-inner">' +
                   '            <img class="margin-top" src="' + blogs[i].image + '" alt="Blog avatar" width="120" height="120" />' +
                   '        </div>' +

                   '        <div class="table-cell content-inner">' +
                   '            <table><td><input class="vote" type="image" src="' + fav_icon + '" alt="fav" data-fav="' + fav_data + '" onclick="subscribeForBlog(this, ' + blogs[i].id + ')" /></td>' +
                   '            <td><h1><a target="_blank" href="/blogs/' + blogs[i].id + '/">' + blogs[i].title + '</a></h1></td></table>' +
                   '            <p class="tiny">' +
                   '                <b class="interest0">Moderator:</b> <a class="usual" target="_blank" href="/profile/' + blogs[i].creator_id + '/">' + blogs[i].creator + '</a>; <b class="interest1">Members:</b> <span id="blog-followers' + blogs[i].id + '">' + blogs[i].cachedMembersNumber + '</span>; <b class="interest2">Rating:</b> ' + blogs[i].cachedBlogRating + '; <b class="interest3">Posts:</b> ' + blogs[i].cachedPostsNumber + '; <b  class="interest4">Created:</b> <span id="' + timerID + '"></span>' +
                   '            </p>' +
                   '            <br />' +

                   '            <p>' + blogs[i].description + '</p>' + '<br />' +
                   '            <a target="_blank" href="/blogs/' + blogs[i].id + '/">Go to posts... </a>' +
                   '        </div>' +
                   '    </div>' +
                   '</div>' +
                   '<br><hr><br>';

        $("#blog_pool").append(text);
    }

    timersUpdate();
}

function constructUsers(users) {
    for (var i = 0; i < users.length; i += 1) {
        if (users[i].image == "") {
            users[i].image = '/static/no_image.jpg';
        }

        var fav_data = users[i].is_subscribed;
        var fav_icon = fav_data == 1 ? '/static/favorite_pressed.png' : '/static/favorite.png';

        var text = '<div>' +
                   '    <div class="table">' +
                   '        <div class="table-cell content-inner">' +
                   '            <img class="margin-top" src="' + users[i].image + '" alt="User avatar" width="40" height="40" />' +
                   '        </div>' +

                   '        <div class="table-cell content-inner">' +
                   '            <table><td><input class="vote" type="image" src="' + fav_icon + '" alt="fav" data-fav="' + fav_data + '" onclick="subscribeForUser(this, ' + users[i].id + ')" /></td>' +
                   '            <td><h1><a target="_blank" href="/profile/' + users[i].id + '/">' + users[i].username + ' (' + users[i].firstname + ' ' + users[i].lastname + ')</a></h1></td></table>' +
                   '            <p class="tiny">' +
                   '                <b class="interest0">Rating:</b> ' + users[i].cachedUserRating + '; <b class="interest1">Posts:</b> ' + users[i].cachedPostsNumber + '; <b class="interest2">Comments:</b> ' + users[i].cachedCommentsNumber + '; <b class="interest3">Followers:</b> <span id="user-followers' + users[i].id + '">' + users[i].cachedFollowersNumber + '</span>; <b  class="interest4">Registered:</b> ' + users[i].registeredDate.substring(0, 10) +
                   '            </p>' +
                   '        </div>' +
                   '    </div>' +
                   '</div>' +
                   '<hr>';

        $("#user_pool").append(text);
    }

    timersUpdate();
}

function voteForPost(btn, type, postId) {
    if (!isAuthenticated()) {
        $("#modal").show();
        $("#modal-login-content").show();
        $("html, body").animate({ scrollTop: 0 }, "slow");

        return;
    }

    var rating = parseInt($("#post-rating" + postId).text());
    var prev = parseInt(btn.dataset.vote);

    if (type == 'up') {
        if (btn.dataset.vote == 1) {
            btn.nextSibling.dataset.vote = btn.dataset.vote = 0;
            btn.src = '/static/upvote.png';
        } else {
            btn.nextSibling.dataset.vote = btn.dataset.vote = 1;
            btn.src = '/static/upvote_pressed.png';
            btn.nextSibling.src = '/static/downvote.png';
        }
    } else {
        if (btn.dataset.vote == -1) {
            btn.previousSibling.dataset.vote = btn.dataset.vote = 0;
            btn.src = '/static/downvote.png';
        } else {
            btn.previousSibling.dataset.vote = btn.dataset.vote = -1;
            btn.src = '/static/downvote_pressed.png';
            btn.previousSibling.src = '/static/upvote.png';
        }
    }

    $("#post-rating" + postId).text(rating + parseInt(btn.dataset.vote) - prev);

    $.ajax({
        type: "POST",
        url: '/api/users.voteForPost',
        data: {
            post_id: postId,
            user_id: getMyId(),
            vote: btn.dataset.vote,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    });
}

function subscribeForPost(btn, postId) {
    if (!isAuthenticated()) {
        $("#modal").show();
        $("#modal-login-content").show();
        $("html, body").animate({ scrollTop: 0 }, "slow");

        return;
    }

    var followers = parseInt($("#post-followers" + postId).text());

    if (btn.dataset.fav == 1) {
        btn.dataset.fav = 0;
        btn.src = '/static/favorite.png';
        $("#post-followers" + postId).text(followers - 1);
    } else {
        btn.dataset.fav = 1;
        btn.src = '/static/favorite_pressed.png';
        $("#post-followers" + postId).text(followers + 1);
    }

    $.ajax({
        type: "POST",
        url: '/api/users.subscribeForPost',
        data: {
            post_id: postId,
            subscriber_id: getMyId(),
            subscribe: btn.dataset.fav,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    });
}

function subscribeForBlog(btn, blogId) {
    if (!isAuthenticated()) {
        $("#modal").show();
        $("#modal-login-content").show();
        $("html, body").animate({ scrollTop: 0 }, "slow");

        return;
    }

    var followers = parseInt($("#blog-followers" + blogId).text());

    if (btn.dataset.fav == 1) {
        btn.dataset.fav = 0;
        btn.src = '/static/favorite.png';
        $("#blog-followers" + blogId).text(followers - 1);
    } else {
        btn.dataset.fav = 1;
        btn.src = '/static/favorite_pressed.png';
        $("#blog-followers" + blogId).text(followers + 1);
    }

    $.ajax({
        type: "POST",
        url: '/api/users.subscribeForBlog',
        data: {
            blog_id: blogId,
            subscriber_id: getMyId(),
            subscribe: btn.dataset.fav,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    });
}

function subscribeForUser(btn, userId) {
    if (!isAuthenticated()) {
        $("#modal").show();
        $("#modal-login-content").show();
        $("html, body").animate({ scrollTop: 0 }, "slow");

        return;
    }

    var followers = parseInt($("#user-followers" + userId).text());

    if (btn.dataset.fav == 1) {
        btn.dataset.fav = 0;
        btn.src = '/static/favorite.png';
        $("#user-followers" + userId).text(followers - 1);
    } else {
        btn.dataset.fav = 1;
        btn.src = '/static/favorite_pressed.png';
        $("#user-followers" + userId).text(followers + 1);
    }

    $.ajax({
        type: "POST",
        url: '/api/users.subscribeForUser',
        data: {
            user_id: userId,
            subscriber_id: getMyId(),
            subscribe: btn.dataset.fav,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    });
}

var timersToUpdate = [];
function timersUpdate() {
    for (var i = 0; i < timersToUpdate.length; i += 1) {
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
