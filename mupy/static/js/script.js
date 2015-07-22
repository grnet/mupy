$('document').ready(function () {
	'use strict';


	var menu = $('#menu');
	var graphsItem = menu.find('.item.graphs')
	var tabs;
	var panes;
	var graphsMenu = menu.find('#graphs_menu');

	function load_menu () {
		// load all the available graphs
		graphsMenu.load(graphsMenu.data('url'), function () {
			graphsItem.find('.fa.loading').addClass('hidden');
			tabs = $('#menu').find('#tabs > li');
			panes = $('#menu').find('#panes > li');

			// Tabs
			tabs.on('click', function () {
				tabs.each(function () {
					$(this).removeClass('active')
				});
				panes.each(function () {
					$(this).removeClass('active')
				});
				$(this).addClass('active');
				$(panes[tabs.index(this)]).addClass('active');
			})
		});
	}

	menu.find('.menu-header').on('click', function () {
		$(this).toggleClass('active');
	});


	// Graphs tree
	menu.on('click', 'li > .expand', function () {
		$(this).parent().toggleClass('active');
	});

	function initialize() {
		load_menu();
	}


	initialize();
});

