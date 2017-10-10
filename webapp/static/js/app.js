document.addEventListener( 'DOMContentLoaded', _ => {
        var elems = document.querySelectorAll('.toggle');
        elems.forEach(function(element) {
            document.addEventListener('click', (element) => toggleElement(element));
        });
    }
);

function toggleElement(element) {
    
}