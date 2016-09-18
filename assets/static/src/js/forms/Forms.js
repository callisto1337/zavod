document.getElementById('btn-login').onclick = function() {
    document.getElementById('form_bg').style.display = 'block';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('form_bg') || event.target == document.getElementsByClassName('form__close')[0])
    {
        document.getElementById('form_bg').style.display = "none";
    }
}


// Form of search
document.getElementById('btn-search').onclick = function() {
    document.getElementById('form-search').className = 'b-menu b-menu_search b-menu_search_toggled';
}

document.getElementById('form__button-cancel').onclick = function() {
    document.getElementById('form-search').className = 'b-menu b-menu_search';
}

