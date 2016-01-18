
function find_query_parameter(name) {
  url = location.href;
  //name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( url );
  return results == null ? null : results[1];
}


// here we set up the configuration of the highCharts chart

var unit_tracker =[];
var counter = 0;
unit_different1=null;
// here we set up the configuration of the highCharts chart
var chart_options = {
	chart: {

		zoomType: 'x',
		resetZoomButton: {
            position: {
                align: 'left', // by default
                verticalAlign: 'bottom', // by default
                x: 0,
                y: 60
            }
        }
	},
    exporting:{
        buttons:{
            contextButton:{

                align: 'right',
                verticalAlign: 'top',

                text: 'print / export chart',
                symbol: 'url(/static/timeseries_viewer/images/print16.png)'
            }
        },
        chartOptions:{
            legend:{
                borderWidth: 0
            }
        },
        sourceWidth: 1200,
        sourceHeight: 600
    },
	title: {
		text: ''
	},
	xAxis: {
		type: 'datetime',
        lineWidth:2,
        lineColor: 'lightgray'
	},
	yAxis: [{
                title: {
                    text: 'Data Value',
                    style: {
                    color: Highcharts.getOptions().colors[1]
                }

                },
                lineWidth:2,
                lineColor: 'lightgray',
                min:0
	        },
        {
            // Secondary yAxis
            gridLineWidth: 1,
            title: {
                text: '',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            min:0,
            lineWidth:2,

        opposite: true
        }
        ],
	legend: {
		align: 'center',
        layout:"vertical",
        itemStyle:{
            fontWeight: 'bold',
            fontSize: '17px'
        },
        title: {text:'Legend'},
        borderColor: '#C98657',
        borderWidth: 1,



	},
	plotOptions: {
		line: {
			color: Highcharts.getOptions().colors[90],
			marker: {
				radius: 2
			},
            size:'100%',
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

    // the res_id can contain multiple IDs separated by comma



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

               // set the y axis title and units
            var units = json.units;
            if(units==null) {
                units = "";
            }

            unit_tracker.push(units);//tracks the units of the different time series
            unit1 = unit_tracker[0];

            unit_different2=null;
            same_unit = 1
            //console.log(units);
            if (unit1 !=units)
            {
              same_unit = 2;//flags which axis is to be used
                console.log(unit_different1)
              if(unit_different1 == null)
              {
                  unit_different1 =units //this tracks the second unit type if there is one
                    console.log(unit_different1)
              }
             };


            //console.log(unit1);
            //console.log(unit_different1);
            //console.log(units);
            if(unit1 != units && unit_different1 !=units )//this triggers if more than different units are used
            {

                console.log(unit1);
                console.log(unit_different1);
                console.log(units);

                chart.hideLoading();
                $('#metadata-loading').hide();
                chart.destroy();

                $("#stats-table").hide();
                $("#metadata-list").hide();
                $('#error-message').text("Error loading time series "+ res_id+". More than two unit types detected.");

                return;

            }




            yaxis=0;
            if (same_unit == 2)
            {

                yaxis = 1;
            }


            var series =
            {
                id: res_id,
                name: json.site_name + ' ' + json.variable_name,
                data: [],
                yAxis: yaxis
            }



            // add the time series to the chart
            series.data = json.for_highchart;

            chart.addSeries(series);

            if (yaxis ==0){
                chart.yAxis[0].setTitle({ text: json.variable_name + ' ' + units });
            }
            else{
                chart.yAxis[1].setTitle({text: json.variable_name + ' ' + units})
            }


            chart.setTitle({ text: "Time Series Viewer" });
            // now we can hide the loading... indicator
            chart.hideLoading();

            // if we have values more than threshold, show title
            if (json.count >= 50000) {
                chart.setTitle({text: 'Showing first 50000 values'})
            }

            // prepare data for the metadata display
            var site_name = json.site_name
            var variable_name = json.variable_name
            var organization = json.organization
            var quality = json.quality
            var method = json.method
            var datatype = json.datatype
            var valuetype = json.valuetype
            var samplemedium = json.samplemedium

            if(site_name==null){
                site_name = "N/A"
            }
            if(variable_name==null){
                variable_name= "N/A"
            }
            if(organization==null){
                organization= "N/A"
            }
            if(quality==null){
                quality= "N/A"
            }
            if(method==null){
                method= "N/A"
            }
            if(datatype==null){
                datatype= "N/A"
            }
            if(valuetype==null){
                valuetype= "N/A"
            }
            if(samplemedium==null){
                samplemedium= "N/A"
            }

            // set the metadata elements content
            var metadata_info =

             "<b>Site:</b>"+site_name +"<br>"+
             "<b>Variable: </b>"+variable_name +"<br>"+
             "<b>Organization: </b>"+organization +"<br>"+
             "<b>Quality: </b>"+quality +"<br>"+
             "<b>Method: </b>"+method +"<br>"+
             "<b>Data Type: </b>"+datatype +"<br>"+
             "<b>Value Type: </b>"+valuetype +"<br>"+
             "<b>Sample Medium: </b>"+samplemedium+"<br>"+'<hr>'


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

            $("#app-content-wrapper #app-content #app-navigation").css({overflow:"auto"});

            $(window).resize();//This fixes an error where the grid lines are misdrawn when legend layout is set to vertical
        },
        error: function() {
            show_error("Error loading time series from " + res_id);
        }
    });
    counter = counter +1
}

var popupDiv = $('#welcome-popup');

$(document).ready(function () {

    $('#metadata-loading').hide();

    var res_id = find_query_parameter("res_id");


    if (res_id == null) {
        if (document.referrer == "https://apps.hydroshare.org/apps/") {
            $('#extra-buttons').append('<a class="btn btn-default btn" href="https://apps.hydroshare.org/apps/">Return to HydroShare Apps</a>');
        }
        popupDiv.modal('show');
    }

    // initialize the chart and set chart height
    var page_height = $(document).height();
    if (page_height > 500) {
        chart_options.chart.height = page_height - 225;
    }

    $('#ts-chart').highcharts(chart_options);

    // add the series to the chart
    var chart = $('#ts-chart').highcharts();

    res_ids = res_id.split(",");


    for  (var  res_id in res_ids)
    {


        add_series_to_chart(chart, res_ids[res_id]);
    };


    // change the app title
    document.title = 'Time Series Viewer';

    // force to adjust chart width when user hides or shows the side bar
    $("#app-content").on("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(event) {
        if (event.originalEvent.propertyName == 'padding-right') {
            $(window).resize(); // this forces the chart to redraw
        }
    });
})
