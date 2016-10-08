/**
 * Реализация показа/скрытия вопроса/ответа на странице FAQ
 */
(function (d, selector) {
    var list = d.getElementsByClassName(selector);

    if (!list.length) {
        return;
    }

    for(var i = 0; i < list.length; i++) {
        list[i].onclick = function () {
            this.classList.toggle('b-faq_expanded');
        }
    }
})(document, 'js-faq');