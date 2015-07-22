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

			panes.on('change', 'ul li input', function () {
				if ($(this).prop('checked')) {
					$(this).closest('li').find('ul li input').each(function () {
						$(this).prop('checked', 'checked');
					});
				} else {
					$(this).closest('li').find('ul li input').each(function () {
						$(this).prop('checked', '');
					});
				}
				refreshChecked();
			});
		});
	}

	menu.find('.menu-header').on('click', function () {
		$(this).toggleClass('active');
	});


	// Graphs tree
	menu.on('click', 'li > .expand', function () {
		$(this).parent().toggleClass('active');
	});

	menu.on('click', 'h5.clear-selection', function () {
		menu.find('#panes input:checked').prop('checked', '');
		refreshChecked();
	});

	function refreshChecked() {
		var selected = [];
		$('#panes li.active li.last input:checked').each(function () {
			selected.push($(this).closest('.last').data('key').replace("graph_",""));
		});
		if (selected.length !== 0) {
			$('.menu-header.submit').removeClass('hidden');
			$('.item.save').removeClass('hidden');
			$('.menu-header.submit .selected').text(selected.length);
			$('h5.clear-selection').removeClass('hidden');
		} else {
			$('.menu-header.submit').addClass('hidden');
			$('.item.save').addClass('hidden');
			$('h5.clear-selection').addClass('hidden');
		}
	}

	$('.loadsearch').on('click', function (ev) {
			ev.preventDefault();
			$('#graphs').load(this.href);
		});

	function initialize() {
		load_menu();
		load_saved_search();
	}

	initialize();
});

