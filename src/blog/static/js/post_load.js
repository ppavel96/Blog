var next_id = 0, load_count = 2;
var is_loading = false;

function load_posts() {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - 100 && !is_loading) {
        is_loading = true;

        $.ajax({
            dataType: "json",
            url: "/ajax/posts/",
            data: { category: '{{category}}', id: next_id.toString(), count: load_count.toString() },
            success: proccess_server_response,
            complete: function () { is_loading = false; }
        });
    }
}

function proccess_server_response(posts) {
    for (var i = 0; i < posts.length; i++) {
        var post_class = (i == 0 && next_id == 0) ? 'post' : 'post indent-needed';

        var text = '<div class="' + post_class + '">' +
                   '    <div class="content-inner">' +
                   '        <h3>' + posts[i].title + '</h3>' +
                   '        <p class="tiny">Опубликовал ' + posts[i].author + ' в ' + posts[i].blog + ' n минут назад</p>' +
                   '        <br />';

        text += posts[i].html_content;

        text +=    '    <a class="content-right right-align-text" href="/posts/1/">Читать комментарии... </a>' +
                   '    </div>' +
                   '</div>';

        $("#post_pool").append(text);
    }

    next_id += posts.length;
}

$(document).ready(load_posts);
$(window).scroll(load_posts);
