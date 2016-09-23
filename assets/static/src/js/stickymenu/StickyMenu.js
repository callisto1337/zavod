/**
 * Реализация "прилепающего" меню
 */
(function () {
	var sticky = {
		/**
		 * Размера скрола, после которого включается "прилепающее"" меню
		 * @type {Number}
		 */
		breakPoint: 180,

		/**
		 * Включен/выключен. По-умолчанию должен быть выключен.
		 * @type {Boolean}
		 */
		active: false,

		/**
		 * Инициализация прилепающего меню
		 * @return {null}
		 */
		init: function () {
			this.sticky = document.getElementById('b-menu');
			this.search = document.getElementsByClassName('b-menu__search')[0];
			this.clone_search = document.getElementsByClassName('b-menu__search')[1];
			this.clone = this.sticky.cloneNode(true);
			this.clone.classList.add('clone');

			document.body.appendChild(this.clone);

			this._initEvents();
			this._scrollHandler();
		},

		/**
		 * Навешивание обработчика для скролла
		 * @TODO сделать `debounce`
		 * @return {null}
		 */
		_initEvents: function () {
			window.addEventListener('scroll', this._scrollHandler.bind(this));
		},

		/**
		 * Обработка скролла
		 * @TODO зарефакторить это
		 * @return {null}
		 */
		_scrollHandler: function () {

			if(window.scrollY > this.breakPoint) {
				this.clone.classList.add('sticky-visible');
				this.active = true;

				if(this.search.classList.contains('b-menu__search_toggled')) {
					this.clone_search.classList.add('sticky-visible');
				}
			} else {
				this.clone.classList.remove('sticky-visible');
				this.active = false;

				if(this.search.classList.contains('b-menu__search_toggled')) {
					this.clone_search.classList.remove('sticky-visible');
				}
			}

			this._handleSubmenu();
		},

		/**
		 * Обработка выпадающего меню
		 * @return {[type]} [description]
		 */
		 _handleSubmenu: function () {}
	};

	// Подключенин при загрузке контента
	document.addEventListener('DOMContentLoaded', sticky.init.bind(sticky));
})();
