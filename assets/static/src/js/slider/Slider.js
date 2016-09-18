/**
 * Реализация слайдера
 */
(function () {
    var slider = {
        /**
         * Элемент, на который включается слайдера
         * @type {String}
         */
        el: '',

        /**
         * Нода со слайдером
         * @type {Node}
         */
        $el: null,

        /**
         * Количество картинок
         * @type {Number}
         */
        count: null,

        /**
         * Ширина слайда
         * @type {Number}
         */
        itemWidth: null,

        /**
         * Количество слайдов на 1 экрана
         * @type {Number}
         */
        itemsPerView: null,

        /**
         * Ширина слайдера
         * @type {Number}
         */
        sliderWidth: null,

        init: function (elID, prevEl, nextEl) {
            this.el = elID || '';
            this.$el = document.getElementById(this.el) || '';

            if (!this.el || !this.$el) {
                return;
            }

            this.count = this.$el.children.length || 0;

            this.sliderWidth = this.$el.clientWidth;
            this.itemWidth = this.$el.children[0].clientWidth;
            this.itemsPerView = this.sliderWidth / this.itemWidth;

            document.getElementById(nextEl).onclick = this.onNextClick.bind(this);
            document.getElementById(prevEl).onclick = this.onPrevClick.bind(this);
        },

        /**
         * Переход вперед
         * @param evt
         */
        onNextClick: function (evt) {
            evt.preventDefault();

            for (var i = 0; i < this.itemsPerView; i++) {
                this.$el.children[0].parentNode.insertBefore(this.$el.children[0], this.$el.children[this.count]);
            }
        },

        /**
         * Переход назад
         * @param evt
         */
        onPrevClick: function (evt) {
            evt.preventDefault();

            for (var i = 0; i < this.itemsPerView; i++) {
                this.$el.children[this.count-1].parentNode.insertBefore(this.$el.children[this.count-1], this.$el.children[0]);
            }
        }
    };

    // Включение слайдера на главной странице
    slider.init('partners', 'arrow-left', 'arrow-right');
})();
