document.addEventListener( 'DOMContentLoaded', _ => {
        document.querySelector('#filter-title').addEventListener('click', toggleFilter);
    }
);

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