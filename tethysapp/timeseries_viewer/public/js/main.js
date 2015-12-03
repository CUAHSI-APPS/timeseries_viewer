
function find_query_parameter(name) {
  url = location.href;
  //name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( url );
  return results == null ? null : results[1];
}

// here we set up the configuration of the highCharts chart
var loading_options = {
        labelStyle: {
        top: '5%',
        left: '5%',
        backgroundImage: 'url("/static/timeseries_viewer/images/ajax-loader.gif")',
        display: 'block',
        width: '134px',
        height: '100px',
        backgroundColor: '#000'
    }
}

// here we set up the configuration of the highCharts chart
var chart_options = {
	chart: {
		zoomType: 'x',
	},
    exporting:{
        buttons:{
            contextButton:{
                text: 'print / export chart',
                symbol: 'url(/static/timeseries_viewer/images/print16.png)'
            }
        }
    },
    loading: {
        //more loading_options can go here..
    },


	title: {
		text: 'Time Series Plot'
	},
	xAxis: {
		type: 'datetime',
        lineWidth:2,
        lineColor: 'lightgray'
	},
	yAxis: {
		title: {
			text: 'Data Value',

		},
        lineWidth:2,
        lineColor: 'lightgray'
	},
	legend: {
		align: 'center',
        itemStyle:{
            fontWeight: 'bold',
            fontSize: '18px'
        },
        title: {text:'Legend'},
        borderColor: '#C98657',
        borderWidth: 1
	},
	plotOptions: {
		line: {
			color: Highcharts.getOptions().colors[0],
			marker: {
				radius: 2
			},
			lineWidth: 1,
			states: {
				hover: {
					lineWidth: 1
				}
			},
			threshold: null
		}
	}
};

// shows an error message in the chart title
function show_error(chart, error_message) {
    chart.legend.group.hide();
    var button = chart.exportSVGElements[0];
    button.destroy();
    chart.hideLoading();
    $('#metadata-loading').hide();
    console.log(error_message);
    $('#error-message').text(error_message);
    chart.setTitle({ text: "" });
}

function add_series_to_chart(chart, res_id) {

    current_url = location.href;
    index = current_url.indexOf("timeseries-viewer");
    base_url = current_url.substring(0, index);

    // in the start we show the loading...
    chart.showLoading();
    $('#metadata-loading').show();

    data_url = base_url + 'timeseries-viewer/chart_data/' + res_id + '/';
    $.ajax({
        url: data_url,
        success: function(json) {

            // first of all check for the status
            var status = json.status;
            if (status !== 'success') {
                show_error(chart, "Error loading time series from " + res_id + ": " + status)
                return;
            }

            var series = {
            id: res_id,
            name: json.site_name + ' ' + json.variable_name,
            data: []
            }

            // add the time series to the chart
            series.data = json.for_highchart;
            chart.addSeries(series);
            chart.yAxis[0].setTitle({ text: json.variable_name + ' ' + json.units });
            chart.hideLoading();

            // set the metadata elements content
            var metadata_info = "<li>" + json.site_name + "</li>" +
            "<ul>" +
            "<li>" + json.variable_name + "</li>" +
            "<li>" + json.organization + "</li>" +
            "<li>" + json.quality + "</li>" +
            "<li>" + json.method + "</li>" +
            "</ul>"

            $('#metadata-list').append(metadata_info);
            $('#metadata-loading').hide();

            // add the row to the statistics table
            var stats_info = "<tr>" +
            "<td>" + json.site_name + "</td>" +
            "<td>" + json.count + "</td>" +
            "<td>" + json.mean + "</td>" +
            "<td>" + json.median + "</td>" +
            "<td>" + json.stdev.toFixed(4) + "</td></tr>";

            $("#stats-table").append(stats_info);

        },
        error: function() {
            show_error("Error loading time series from " + res_id);
        }
    });
}


$(document).ready(function () {

    $('#metadata-loading').hide();

    var res_id = find_query_parameter("res_id");

    // initialize the chart
    $('#ts-chart').highcharts(chart_options);

    // add the series to the chart
    var chart = $('#ts-chart').highcharts();
    add_series_to_chart(chart, res_id);
})
