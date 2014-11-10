
$('document').ready(function () {
	'use strict';
	var selected = [];
	var readonly = $('.menu-wrapper').hasClass('read_only');

	$('.menu-header').on('click', function (e) {
		// $('.menu-header').not(this).removeClass('active');
		$(this).toggleClass('active');
	});

	function getChildren(data) {
		if (data) {
			var html = '<ul>';
			for (var i=0; i<data.length; i++) {
				html +='<li ';
				if (!data[i].children) {
					html += 'class="last"';
					html += 'data-img="' + data[i].url +'"';
					html += 'data-page="' + data[i].pageurl + '"';
					html += 'data-key="' + data[i].key + '"';
					html += 'data-host="' + data[i].nodename + '"';
					html += 'data-type="' + data[i].graphname + '"';
				}
				html += '><label><input type="checkbox" ';
				if (readonly) {
					html += ' disabled '
				}
				html += '><span class="ui-input"><i class="checked fa fa-check-circle"></i><i class="unchecked fa fa-circle-thin"></i></span>'+ data[i].title + '</label>'
				if (data[i].children) {
					html += '<span class="expand"><i class="plus fa fa-plus-square"></i><i class="minus fa fa-minus-square"></i></span>';
					html += getChildren(data[i].children);
				}
				html +='</li>';
			}
			html += '</ul>';
			return html;
		} else {
			return ''
		}
	}

	function loadTab(tab) {
		$(tab).siblings().each(function () {
			$(this).removeClass('active');
		})
		$(tab).addClass('active');
		$('#panes li').each(function () {
			$(this).removeClass('active');
		});
		$($('#panes > li')[$('#tabs li').index(tab)]).addClass('active');
		if (!$(tab).hasClass('loaded')) {
			var url = $(tab).data('href');
			var html = '<ul class="active">';
			$.getJSON(url, function (data) {
				if (data.length === 0) {
					swal({
						title: "No access",
						text: "You have no access to any nodes... Please ask your admin to give you some!",
						type: "warning",
						confirmButtonClass: "btn-danger",
						confirmButtonText: "OK",
					});
				}
				for (var i=0; i < data.length; i++) {
					html +='<li';
					if (!data[i].children) {
						html += 'class="last"';
					}
					html += '><label><input type="checkbox"';
					if (readonly) {
						html += ' disabled '
					}
					html += '><span class="ui-input"><i class="checked fa fa-check-circle"></i><i class="unchecked fa fa-circle-thin"></i></span>'+ data[i].title + '</label>'
					if (data[i].children) {
						html += '<span class="expand"><i class="plus fa fa-plus-square"></i><i class="minus fa fa-minus-square"></i></span>';
						html += getChildren(data[i].children);
					}
					html += '</li>';
				}
				html += '</ul>';
				$('#panes li.active').html(html);
				$(tab).addClass('loaded');
			});
		}
	}

	function loadSavedSearches(callback) {
		if (!callback) {
			callback = function () {};
		}
		var html =  '';
		$.getJSON($('#menu .item.saved_searches').data('url'), function (data) {
			if (data.saved.length) {
				$('#menu .item.saved_searches').removeClass('hidden');
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
				$('#menu .item.saved_searches').addClass('hidden');
			}
			$('#menu .item.saved_searches .menu-content').html(html);
			callback();
		});

	}

	if (!readonly) {
		$('#menu .item.saved_searches .menu-content').on('click', '.delete', function () {
			$.getJSON($(this).data('url'), function (data) {
				swal("Deleted", data.result, "success")
				loadSavedSearches();
			});
		});
	}

	if (!readonly) {
		$('#menu .item.saved_searches .menu-content').on('change', 'label input', function () {
			$.getJSON($(this).closest('label').data('url'), function (data) {
				if (data.errors) {
					swal('Error', 'An error occured', 'warning');
				}
				loadSavedSearches();
			});
		});
	}

	if (!readonly) {
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
			$("#id_display_type").val($('#tabs li').index($('#tabs li.active')));
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
	}

	$('#menu .item.saved_searches').on('click', 'a.loadsearch', function (ev) {
		$('a.loadsearch').removeClass('active');
		$(this).addClass('active');
		ev.preventDefault();
		$('#panes li input').prop('checked', '');
		$.getJSON($(this).prop('href'), function (data) {
			var selectedItems = data.result.split(',');
			$($('#tabs li')[data.display_type]).trigger('click');
			var items = $('#panes .active li.last');
			for (var i in selectedItems) {
				var current = items.filter('[data-key="graph_' + selectedItems[i] +'"]');
				current.find('input').prop('checked', 'checked');
			}
			$('.menu-header.submit').trigger('click');
			refreshChecked();
		});
	});

	function loadDefaultSearch() {
		$('#menu .item.saved_searches input:checked').closest('div').find('a').trigger('click');
	};

	function initialize() {
		loadTab($('#tabs li.active'));
		loadSavedSearches(function () {
			loadDefaultSearch();
		});

	}

	if (!readonly) {
		$('.clear-selection').on('click', function () {
			$('#menu #panes input:checked').prop('checked', '');
			refreshChecked();
		});
	}

	function refreshChecked() {
		selected = [];
		$('#panes li.active li.last input:checked').each(function () {
			selected.push($(this).closest('.last').data('key').replace("graph_",""));
		});
		if (selected.length !== 0) {
			$('.menu-header.submit').removeClass('hidden');
			$('.item.save').removeClass('hidden');
			$('.menu-header.submit .selected').text(selected.length);
		} else {
			$('.menu-header.submit').addClass('hidden');
			$('.item.save').addClass('hidden');
		}
	}

	$('#graphs').on('click', function () {
		$('#menu-toggle').prop('checked', '');
	});

	$('#tabs li').on('click', function () {
		loadTab(this);
		refreshChecked();
	});

	$('#panes li').on('click', '.expand', function () {
		$(this).toggleClass('open')
		$(this).parent().find('> ul').toggleClass('active');
	});

	$('.submit').on('click', function () {
		$('#menu').removeClass('initial');
		var html = '';
		var graphsDiv = $('#graphs');
		var period = $('input:radio[name=period]:checked').val();
		var grouping = $('input:radio[name=grouping]:checked').val();
		var refresh = $('input:radio[name=refresh]:checked').val();
		var graphs = [];
		$('#panes li.active li.last input:checked').each(function () {
			var current = $(this).closest('li');
			var randomNo = Math.floor(Math.random()*9999999);
			graphs.push({'host': current.data('host'), 'type': current.data('type'), 'html': '<a data-host="' + current.data('host') + '" class="col-4" href="' + current.data('page') + '" target="_blank"><h4>' + current.data('host') + ' - ' + current.data('type') + '</h4><img src="' + current.data('img') + '-' + period + '.png?r=' + randomNo + '"  width="479" height="280"></a>'});
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

	$('#panes li').on('change', 'ul li input', function () {
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

	initialize();
});

