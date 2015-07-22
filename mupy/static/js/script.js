$('document').ready(function () {
	'use strict';

	function initialize() {
		console.log('init');
	}

	var menu = $('#menu');
	menu.find('.menu-header').on('click', function () {
		$(this).toggleClass('active');
	});

	menu.on('click', 'li > .expand', function () {
		console.log('clicked');
		$(this).parent().toggleClass('active');
	});

	initialize();
});

