
function find_query_parameter(name) {
  url = location.href;
  //name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( url );
  return results == null ? null : results[1];
}


var chart_options = {
	chart: {
		zoomType: 'x',
	},
	title: {
		text: 'Time Series Plot'
	},
	xAxis: {
		type: 'datetime'
	},
	yAxis: {
		title: {
			text: 'Data Value'
		}
	},
	legend: {
		align: 'center'
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


function add_series_to_chart(chart, res_id) {

    current_url = location.href;
    index = current_url.indexOf("timeseries-viewer");
    base_url = current_url.substring(0, index);

    data_url = base_url + 'timeseries-viewer/chart_data/' + res_id + '/';
    $.ajax({
        url: data_url,
        success: function(json) {

            var series = {
            id: res_id,
            name: json.site_name + ' ' + json.variable_name,
            data: []
            }

            series.data = json.for_highchart;
            chart.addSeries(series);
            chart.yAxis[0].setTitle({ text: json.variable_name + ' ' + json.units });
        },
        cache: false
    });

}


$(document).ready(function () {

    var res_id = find_query_parameter("res_id");

    // initialize the chart
    $('#ts-chart').highcharts(chart_options);

    // add the series to the chart
    var chart = $('#ts-chart').highcharts();
    add_series_to_chart(chart, res_id);
})
