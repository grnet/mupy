
$('document').ready(function () {
	'use strict';
	var selected = [];

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
				}
				html += '><label><input type="checkbox"><span class="ui-input"><i class="checked fa fa-check-circle"></i><i class="unchecked fa fa-circle-thin"></i></span>'+ data[i].title + '</label>'
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
					alert('You have no access to any nodes... Please ask your admin to give you some!')
				}
				for (var i=0; i < data.length; i++) {
					html +='<li';
					if (!data[i].children) {
						html += 'class="last"';
					}
					html += '><label><input type="checkbox"><span class="ui-input"><i class="checked fa fa-check-circle"></i><i class="unchecked fa fa-circle-thin"></i></span>'+ data[i].title + '</label>'
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

	$('#menu .item.saved_searches .menu-content').on('click', '.delete', function () {
		$.getJSON($(this).data('url'), function (data) {
			alert(data.result);
			loadSavedSearches();
		});
	});


	$('#menu .item.saved_searches .menu-content').on('change', 'label input', function () {
		$.getJSON($(this).closest('label').data('url'), function (data) {
			if (data.errors) {
				alert('Error');
			}
			loadSavedSearches();
		});
	});

	$('#saveQueryForm').on('submit', function (e) {
		e.preventDefault();
		if (selected.length == 0){
			alert('Select at least a graph from the left menu');
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
			alert(out.result);
			loadSavedSearches();
		});
	})

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
		$('#panes li.active li.last input:checked').each(function () {
			var current = $(this).closest('li');
			var period = $('input:radio[name=period]:checked').val();
			var randomNo = Math.floor(Math.random()*9999999);
			html += '<a class="col-4" href="' + current.data('page') + '" target="_blank"><img src="' + current.data('img') + '-' + period + '.png?r=' + randomNo + '"  width="479" height="280"></a>';
		});
		graphsDiv.html(html);

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


// 		var showGraphs = false;
// 		var allLoaded = false;
// 		var refreshId = false;
// 		var catLoaded = false;
// 		var refreshTime = 5;
// 		var activeTabIndex = false;
// 		graphs_arr = new Array();
// 		var searchesNames = new Array();
// 		var selectedKeys = new Array();
// 		urlTabArray = ["{% url getjson_all user.pk %}", "{% url getjson_category user.pk %}"];
// 		countGraphs = 0;
// 		var loaded_graphs = new Array();
// 		{% if new_window %}
// 			mydata = "{{new_window.result}}";
// 			//var nwdata = $.parseJSON(mydata)
// 			var darray = ("{{new_window.result}}").split(',');
// 			loaded_graphs = darray;

// 		{% endif %}

// 		{% if saved %}
// 			{% for sav in saved %}
// 				searchesNames.push("{{sav}}");
// 			{% endfor %}
// 		{% endif %}

// 		$(document).ready(function(){

// 			{% if new_window %}
// 				$("#tabs").hide();
// 				$("#counted_graphs_holder").hide();
// 				$("#user_details").hide();
// 			{% endif %}
// 			$("#counted_graphs").html("0 graphs selected");
// 			$("#graphs").empty();
// 			$("#save_dialog").hide();
// 			$( "#slider" ).slider({
// 				range: "max",
// 				min: 3,
// 				max: 15,
// 				value: 5,
// 				slide: function( event, ui ) {
// 					refreshTime = ui.value ;
// 					if (refreshId != false){
// 						clearInterval(refreshId);
// 					}
// 					$( "#refreshIndicator" ).text( ui.value );
// 				}
// 			});
// 			$( "#refreshIndicator" ).text( $( "#slider" ).slider( "value" ) );

// 			$( "#tabs" ).tabs({
// 				   show: function(event, ui) {
// 					   clearGraphData();
// 					   if (ui.index == 0 || ui.index == 1){
// 						   activeTabIndex = ui.index;
// 						   $("#tree_menu_"+ui.index).dynatree({
// 								checkbox: true,
// 								selectMode: 3,
// 								debugLevel: 0,
// 								ajaxDefaults: {
// 							        cache: true, // false: Append random '_' argument to the request url to prevent caching.
// 							    },
// 							    initAjax:
// 							    {
// 							    	url: urlTabArray[ui.index],
// 							    },
// 							    onPostInit: function(isReloading, isError) {
// 							    	allLoaded = true;
// 									$("#tree_menu_"+activeTabIndex).dynatree("getRoot").visit(function(node){
// 										if (node.hasChildren() == false){
// 											nodekey = node.data.key.replace("graph_", "");
// 										}
// 										else{
// 											nodekey = node.data.key;
// 										}
// 						    		 	if ($.inArray(nodekey, loaded_graphs) != -1){
// 											node.select(true);
// 						    		 	}
// 						    		 	else{
// 						    		 		node.select(false);
// 						    		 	}
// 									});
// 									{% if new_window %}
// 										$("#fetch").click();
// 									{% endif %}
// 							    },
// 							    onSelect: function(select, node) {
// 							    	var selNodes = node.tree.getSelectedNodes();
// 							    	clearGraphData();
// 								    var selKeys = $.map(selNodes, function(node){
// 									    if (node.hasChildren() == false){
// 									    		countGraphs = countGraphs +1;
// 									    		graphObj = new Object();
// 									    		graphObj.nodename = node.data.nodename;
// 									    		graphObj.graphname = node.data.graphname;
// 									    		graphObj.title = node.data.title;
// 									    		graphObj.imgurl = node.data.url
// 									    		graphObj.pageurl = node.data.pageurl
// 									    		graphObj.nodeurl = node.data.nodeurl
// 									    		graphs_arr.push(graphObj);
// 									    		selectedKeys.push(node.data.key.replace("graph_",""));
// 									    		$("#counted_graphs").html(selectedKeys.length+' graphs selected');
// 											}
// 								    });
// 							    },
// 							});
// 					   }

// 				   },
// 				   select: function(event, ui) {
// 					   if (allLoaded == true){
// 						   $("#tree_menu_"+activeTabIndex).dynatree("getRoot").visit(function(node){
// 								node.select(false);
// 							});
// 					   }
// 				   }
// 				});
// 			$("#fetch")
// 				.button()
// 				.click(function(){
// 					if (selectedKeys.length == 0){
// 						alert("Select at least a graph from the left menu");
// 						return false;
// 					}
// 					$("#graphs").empty();
// 					fetchGraphs();
// 					if (refreshId != false){
// 						clearInterval(refreshId);
// 					}
// 					refreshId = setInterval(function(){
// 						$("#graphs").empty();
// 						fetchGraphs();
// 					}, refreshTime*1000*60);
// 					return false;
// 				});
// 			$("#deselect")
// 			.click(function(){
// 				if (refreshId != false){
// 					clearInterval(refreshId);
// 				}
// 				if (allLoaded == true){
// 					$("#tree_menu_"+activeTabIndex).dynatree("getRoot").visit(function(node){
// 							node.select(false);
// 						});
// 				   }
// 			clearGraphData();
// 			return false
// 			});

// 			$("#save")
// 				.button()
// 				.click(function(){
// 					if (selectedKeys.length == 0){
// 						alert("Select at least a graph from the left menu")
// 						return false;
// 					}
// 				$("#save_dialog").toggle("slow");
// 				return false
// 			});

// 			$("#saveThisQuery")
// 			.button()
// 			.click(function(){
// 				if (selectedKeys.length == 0){
// 					alert("Select at least a graph from the left menu")
// 				}
// 				else{
// 					if ($.inArray($("#id_description").val(), searchesNames) != -1){
// 						var r=confirm("There is a saved search with the same name: "+$("#id_description").val()+"\n"
// 								+"Press OK to ovewrite or Cancel to cancel save");
// 						if (r==false){
// 							$("#id_is_edit").empty();
// 							return false;
// 						}
// 						else{
// 							$("#id_is_edit").val('edit');
// 						}
// 	    		 	}

// 					$("#id_graphs").val(selectedKeys.join(','));
// 					$("#id_display_type").val(activeTabIndex);
// 					data = $("#saveQueryForm").serialize();
// 					$.post('{% url save_search %}', data,
// 						function(out) {
// 						  alert(out.result);
// 						  if (out.errors == "None"){
// 							  searchesNames.push($("#id_description").val());
// 						  }
// 						  $("#id_is_edit").empty();
// 						  $("#save_dialog").toggle("slow");
// 						}
// 					);

// 				}
// 				return false;
// 			});

// 			$( "#dialog" ).dialog({
// 				autoOpen: false,
// 				width: 600,
// 				show: "blind",
// 				hide: "blind"
// 			});



// 		});

// 		function clearGraphData(){
// 			graphs_arr = new Array();
// 			countGraphs = 0;
// 			$("#counted_graphs").html("0 graphs selected");
// 			$("#graphs").empty();
// 			selectedKeys = new Array();
// 		}

// 		function fetchGraphs(){
// 			var period = $("input:radio[name=period]:checked").val();
// 			var grouptype = $("input:radio[name=grouping]:checked").val();
// 			grouppedgraphs = groupGraphs(grouptype);
// 			for (var j=0, k=grouppedgraphs.length; j<k; j++){
// 				graph_group = grouppedgraphs[j];
// 				$("#graphs").append("<div class='group_graph_holder'><h3 class='group_title'><a href='#group'"+j+">"+graph_group[grouptype]+"</a></h3><ul id='graph_group_"+j+"' class='graphs_no_list'></ul></div>");
// 				$(".group_graph_holder").accordion(
// 							{collapsible: true,
// 							autoHeight: false,
// 							});
// 				for(var i=0, l=graph_group.graphs.length; i<l; i++){
// 					graphitem = graph_group.graphs[i];
// 					var randomNo = Math.floor(Math.random()*9999999);
// 					$("#graph_group_"+j+"").append(
// 						"<li class='graph_li'>"+
// 							"<div class='graph_blockfloat'>"+
// 							"<a href='"+graphitem.nodeurl+"' target='_blank'>"+
// 								graphitem.nodename+"</a>"+
// 								"<br>"+
// 								"<a href='"+graphitem.pageurl+"' target='_blank'>"+
// 								graphitem.graphname+"<br><br>"+
// 								"<img class='graph_class' width='479' height='280' src='"+graphitem.imgurl+"-"+period+".png?r="+randomNo+"'/></a>"+
// 						"</div></li>"
// 					);
// 				}
// 			}
// 		}

// 		function groupGraphs(type){
// 			graphGroupArr = new Array();
// 			graphGroup = new Object();
// 			graphGroup.graphs = new Array();
// 			for(var i=0, l=graphs_arr.length; i<l; i++){
// 				graphitem = graphs_arr[i];
// 				if (type == 'nogroup')
// 				{
// 					graphGroup[type] = "No grouping"
// 					graphGroup.graphs.push(graphitem);
// 				}
// 				else
// 				{
// 					found = findIndexByKeyValue(graphGroupArr, type, graphitem[type]);
// 					if (found == null){
// 						graphGroup = new Object();
// 						graphGroup.graphs = new Array();
// 						graphGroup[type] = graphitem[type];
// 						graphGroup.graphs.push(graphitem);
// 						graphGroupArr.push(graphGroup);
// 					}
// 					else{
// 						graphGroupArr[found].graphs.push(graphitem)
// 					}
// 				}
// 			}
// 			if (type == 'nogroup')
// 			{
// 				graphGroupArr.push(graphGroup);
// 			}
// 			return graphGroupArr;

// 		}
// 		function findIndexByKeyValue(obj, key, value)
// 		{
// 		    for (var i = 0; i < obj.length; i++) {
// 		        if (obj[i][key] == value) {
// 		            return i;
// 		        }
// 		    }
// 		    return null;
// 		}
