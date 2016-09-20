document.getElementById('btn-search').onclick = function() {
    document.getElementById('b-menu__search').className = 'b-menu b-menu__search b-menu__search_toggled';
}

document.getElementById('form-search__button-cancel').onclick = function() {
    document.getElementById('b-menu__search').className = 'b-menu b-menu__search';
}