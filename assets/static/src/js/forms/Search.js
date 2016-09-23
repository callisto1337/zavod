window.onload = function() {
    menu_search = document.getElementsByClassName('b-menu__search')[0];
    menu_search_clone = document.getElementsByClassName('b-menu__search')[1];
    menu_search_cancel = document.getElementsByClassName('form-search__button_cancel')[0];
    menu_search_clone_cancel = document.getElementsByClassName('form-search__button_cancel')[1];

    btn_search = document.getElementsByClassName('b-menu__item-link_search')[0];
    btn_search_clone = document.getElementsByClassName('b-menu__item-link_search')[1];

    btn_search.onclick = function () {
        menu_search.classList.add('b-menu__search_toggled');
    }

    btn_search_clone.onclick = function() {
        menu_search.classList.add('b-menu__search_toggled');
        menu_search_clone.classList.add('sticky-visible');
    }

    menu_search_cancel.onclick = function () {
        menu_search.classList.remove('b-menu__search_toggled');
    }

    menu_search_clone_cancel.onclick = function () {
        menu_search_clone.classList.remove('sticky-visible');
        menu_search.classList.remove('b-menu__search_toggled');
    }
}
