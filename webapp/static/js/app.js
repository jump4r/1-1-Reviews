document.addEventListener( 'DOMContentLoaded', _ => {
        loadBookmarks();
        document.querySelector('#filter-title').addEventListener('click', toggleFilter);
        var bookmarks = document.querySelectorAll('.bookmark-icon');
        bookmarks.forEach(function(bookmark) {
            bookmark.addEventListener('click', bookmarkItem);
        });
    }
);

function loadBookmarks() {
    items = window.localStorage.getItem('bookmarks').split(',');
    items.forEach( function(item) {
        img = document.getElementById(item).firstElementChild.getElementsByTagName('img')[1];
        img.src = './static/icons/heartfull.png';
    });
}

function toggleFilter() {
    style = getStyle('filter-form', 'display');

    if (style === 'none') {
        document.querySelector('#filter-form').style.display = 'block';
        document.querySelector('#filter-title').innerHTML = 'Hide Filter'
    }

    else if (style === 'block') {
        document.querySelector('#filter-form').style.display = 'none';
        document.querySelector('#filter-title').innerHTML = 'Show Filter'
    }
}

function getStyle(id, name) {
    var element = document.getElementById(id);
    return element.currentStyle ? element.currentStyle[name] : window.getComputedStyle ? window.getComputedStyle(element, null).getPropertyValue(name) : null;
}

function bookmarkItem() {
    storage = window.localStorage;

    if (storage.getItem('bookmarks') === null) {
        this.src = "./static/icons/heartfull.png"
        window.localStorage.setItem("bookmarks", this.parentElement.parentElement.id.toString());
        return;
    }

    else {
        bookmarks = storage.getItem('bookmarks');
        items = bookmarks.split(',');
        id = this.parentElement.parentElement.id.toString()

        if (!arrayContains(id, items)) {
            this.src = "./static/icons/heartfull.png"
            items.push(id);
            storage.setItem('bookmarks', items.join(','));
        }

        else {
            this.src = "./static/icons/heartempty.png"
            items.splice(items.indexOf(id), 1);
            storage.setItem('bookmarks', items.join(','));
        }
    }
}

function arrayContains(needle, haystack) {
    return (haystack.indexOf(needle) > -1);
}