$('document').ready(function () {
	'use strict';


	var menu = $('#menu');
	var graphsItem = menu.find('.item.graphs')
	var tabs;
	var panes;
	var graphsMenu = menu.find('#graphs_menu');
	var selected = [];

	$('.fullscreen').on('click', function () {
		$('#mupy_page').toggleClass('full');
	});

	function load_menu () {
		// load all the available graphs
		graphsMenu.load(graphsMenu.data('url'), function () {
			menu.removeClass('loading');
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
		selected = [];
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

	menu.find('.item.saved_searches').on('click', 'a.loadsearch', function (ev) {
		$('a.loadsearch').removeClass('active');
		$(this).addClass('active');
		ev.preventDefault();
		panes.find('li.active input').prop('checked', '');
		$.getJSON($(this).prop('href'), function (data) {
			var selectedItems = data.result.split(',');
			$(tabs[data.display_type]).trigger('click');
			var items = $('#panes .active li.last');
			for (var i in selectedItems) {
				var current = items.filter('[data-key="graph_' + selectedItems[i] +'"]');
				current.find('input').prop('checked', 'checked');
				current.parents().filter('li').each(function (item) {
					$(this).find('> label input').prop('checked', 'checked');
				});
			}
			$('.menu-header.submit').trigger('click');
			refreshChecked();
		});
	});

	function initialize() {
		load_menu();
	}

	$('.submit').on('click', function () {
		var html = '';
		var graphsDiv = $('#graphs');
		var period = $('input:radio[name=period]:checked').val();
		var grouping = $('input:radio[name=grouping]:checked').val();
		var refresh = $('input:radio[name=refresh]:checked').val();
		var graphs = [];
		$('#panes li.active li.last input:checked').each(function () {
			var current = $(this).closest('li');
			var randomNo = Math.floor(Math.random()*9999999);
			var baseurl = $($(this).parents().filter('li[data-baseurl]')[0]).data('baseurl');
			var name = $($(this).parents().filter('li[data-nodename]')[0]).data('nodename');
			var host = $($(this).parents().filter('li[data-nodeurl]')[0]);
			graphs.push({'host': host.find('> span').text(), 'type': current.data('type'), 'html': '<a data-host="' + name + '" class="col-4" href="' + baseurl + host.data('nodeurl') + '" target="_blank"><h4>' + name + ' - ' + current.data('type') + '</h4><img src="' + baseurl + current.data('img') + '-' + period + '.png?r=' + randomNo + '"  width="479" height="280"></a>'});
		});
		if  (grouping === 'nodename') {
			graphs.sort(function (a, b) {
				if (a.host > b.host) {
					return 1;
				}
				if (a.host < b.host) {
					return -1;
				}
				return 0;
			});
		} else if (grouping === 'graphname') {
			graphs.sort(function (a, b) {
				if (a.type > b.type) {
					return 1;
				}
				if (a.type < b.type) {
					return -1;
				}
				return 0;
			});
		}
		for (var item in graphs) {
			html += graphs[item].html;
		}
		if (refresh !== '0') {
			setInterval(function () {
				graphsDiv.html(html);
			}, parseInt(refresh, 10) * 60);
		} else {
			graphsDiv.html(html);
		}
	});

	// delete saved search
	menu.find('.item.saved_searches .menu-content').on('click', '.delete', function () {
		$.getJSON($(this).data('url'), function (data) {
			swal("Deleted", data.result, "success")
			loadSavedSearches();
		});
	});


	// change default search
	menu.find('.item.saved_searches .menu-content').on('change', 'label input', function () {
		$.getJSON($(this).closest('label').data('url'), function (data) {
			if (data.errors) {
				swal('Error', 'An error occured', 'warning');
			}
			loadSavedSearches();
		});
	});

	$('#saveQueryForm').on('submit', function (e) {
		e.preventDefault();
		if (selected.length == 0){
			swal('Warning','Select at least a graph from the left menu', 'warning');
		} else{
			if ($.inArray($("#id_description").val(), []) != -1){
				var r=confirm('There is a saved search with the same name: '+ $("#id_description").val()+ '\nPress OK to ovewrite or Cancel to cancel save');
				if (r==false){
					$("#id_is_edit").empty();
					return false;
				}
				else{
					$("#id_is_edit").val('edit');
				}
		 	}
		}
		$("#id_graphs").val(selected.join(','));
		$("#id_display_type").val(tabs.index(tabs.filter('.active')));
		var formData = $(this).serialize();
		$.post($(this).data('post'), formData, function(out) {
			if (out.errors) {
				swal('Error', out.result, 'warning');
			} else {
				swal('Success', out.result, 'success');
				loadSavedSearches();
			}
		});
	})

	function loadSavedSearches(callback) {
		if (!callback) {
			callback = function () {};
		}
		var html =  '';
		$.getJSON(menu.find('.item.saved_searches').data('url'), function (data) {
			if (data.saved.length) {
				menu.find('.item.saved_searches').removeClass('hidden');
				for (var i=0; i< data.saved.length; i++) {
					html += '<div><a class="loadsearch" href="' + data.saved[i].url + '">' + data.saved[i].description + '</a>';
					html += '<label data-url="' + data.saved[i].default_url + '"><input type="radio"';
					if (data.saved[i].default === true) {
						html += 'checked="checked"';
					}
					html +=' name="default-search"><i class="fa default-search fa-star"></i><i  class="fa default-search-empty fa-star-o"></i>';
					html += '</label><i data-url="' + data.saved[i].delete_url + '" class="fa fa-times delete"></i></div>';
				}
			} else {
				menu.find('.item.saved_searches').addClass('hidden');
			}
			menu.find('.item.saved_searches .menu-content').html(html);
			callback();
		});

	}


	initialize();
});

