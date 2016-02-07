function find_query_parameter(name) {
  url = location.href;
  //name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( url );
  return results == null ? null : results[1];
}


// here we set up the configuration of the highCharts chart
var data = [];
var unit_tracker =[];
var counter = 0;
unit_different1=null;
counter1 =[];
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

            lineWidth:2,

        opposite: true
        }
        ],
	legend: {




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
var number2 = -1

function add_series_to_chart(chart, res_id,number1) {

    console.log(number1)

    current_url = location.href;
    index = current_url.indexOf("timeseries-viewer");
    base_url = current_url.substring(0, index);

    // in the start we show the loading...



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

            if (unit1 !=units)
            {
              same_unit = 2;//flags which axis is to be used

              if(unit_different1 == null)
              {
                  unit_different1 =units //this tracks the second unit type if there is one

              }
             };

            //console.log(unit1);
            //console.log(unit_different1);
            //console.log(units);
            if(unit1 != units && unit_different1 !=units )//this triggers if more than different units are used
            {
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
                name:  'Site: '+json.site_name
                +'. Variable: ' + json.variable_name,
                data: [],
                yAxis: yaxis
            }

            // add the time series to the chart
            series.data = json.for_highchart;

            chart.addSeries(series);
            //console.log(json.smallest_value)
            if (yaxis ==0){
                chart.yAxis[0].setTitle({ text: json.variable_name + ' ' + units });
                //chart.yAxis[0].setExtremes(json.smallest_value,null,true,false);
            }
            else{
                chart.yAxis[1].setTitle({text: json.variable_name + ' ' + units})
                //chart.yAxis[1].setExtremes(json.smallest_value,null,true,false);
            }

            chart.setTitle({ text: "Time Series Viewer" });
            // now we can hide the loading... indicator
            //chart.hideLoading();
            chart.legend.group.hide();
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

             "<b>Site: </b>"+site_name +"<br>"+
             "<b>Variable: </b>"+variable_name+","+ datatype+","+valuetype +"<br>"+
             "<b>Organization: </b>"+organization +"<br>"+
             "<b>Quality: </b>"+quality +"<br>"+
             "<b>Method: </b>"+method +"<br>"+
             "<b>Sample Medium: </b>"+samplemedium+"<br>"

            $('#metadata').append(metadata_info);
            $('#metadata_test1').append(metadata_info);
            $('#metadata-loading').hide();

            // add the row to the statistics table
            number2 = number2+1//keeps track of row number for stats table
            number  = number2;
            var stats_info = "<tr>" +
            "<td style='text-align:center' bgcolor = "+chart.series[number].color+"><input id ="+number
                + " type='checkbox'onClick ='myFunc(this.id);'checked = 'checked'>" + "</td>" +
            "<td>" + json.site_name + "</td>" +
            "<td>" + variable_name+", "+ datatype+", "+valuetype  + "</td>" +
            "<td>" + organization + "</td>" +
            "<td>" + quality + "</td>" +
            "<td>" + method + "</td>" +
            "<td>" + samplemedium + "</td>" +
            "<td>" + json.count + "</td>" +
            "<td>" + json.mean + "</td>" +
            "<td>" + json.median + "</td>" +
            "<td>" + json.stdev.toFixed(4) + "</td></tr>";

            //$("#stats-table").append(stats_info);

            //new table
            var site_name = json.site_name
            var variable_name = json.variable_name
            var unit = json.units
            var organization = json.organization
            var quality = json.quality
            var method = json.method
            var datatype = json.datatype
            var valuetype = json.valuetype
            var samplemedium = json.samplemedium
            var count = json.count
            var mean = json.mean
            var median = json.median
            var stdev = json.stdev
            var timesupport = json.timesupport
            var timeunit = json.timeunit
            var sourcedescription = json.sourcedescription


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
            if(unit==null){
                unit= "N/A"
            }
            if(timesupport==null){
                timesupport= "N/A"
            }
            if(timeunit==null){
                timeunit= "N/A"
            }
            if(sourcedescription==null){
                sourcedescription= "N/A"
            }
            if(samplemedium==null){
                samplemedium= "N/A"
            }



            var legend = "<td style='text-align:center' bgcolor = "+chart.series[number].color+"><input id ="+number
                + " type='checkbox' STYLE ='color:"+chart.series[number].color+"' onClick ='myFunc(this.id);'checked = 'checked'>" + "</td>"
            var dataset = {legend:legend,organization:organization,name:site_name,variable:variable_name,unit:unit,samplemedium:samplemedium,count:count,
                quality:quality,method:method,datatype:datatype,valuetype:valuetype, timesupport:timesupport,timeunit:timeunit,
                sourcedescription:sourcedescription,
                mean:mean,median:median,stdev:stdev}
            var table = $('#example').DataTable();
            table.row.add(dataset).draw();

            //end new table

            if (number == number1-1)//checks to see if all the data is loaded before displaying
            {
                finishloading();
            }
            $(window).resize();//This fixes an error where the grid lines are misdrawn when legend layout is set to vertical
        },
        error: function() {
            show_error("Error loading time series from " + res_id);
        }
    });
}


$('#button').click(function() {
    $('#stats-table').toggle();
});
function myFunc(id){
    var chart1 = $('#ts-chart').highcharts();
    var series = chart1.series[id];
        if (series.visible) {
            series.hide();
        } else {
            series.show();
        }
}

var popupDiv = $('#welcome-popup');


    //end new table
$(document).ready(function (callback) {
    var res_id = find_query_parameter("res_id");

    var table = $('#example').DataTable( {
        "createdRow":function(row,data,dataIndex)
        {

            $('td',row).eq(0).css("backgroundColor", chart.series[number].color)
            console.log("cell added")
        },
        data: data,
        "columns":
            [
            {   "className": "legend",
                "data": "legend" },
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { "data": "organization" },
            { "data": "name" },
            { "data": "variable" },
            { "data": "unit" },
            { "data": "samplemedium" },
            { "data": "count" }
            ],
        "order": [[1, 'asc']]
    } );
    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            box();
            var chart = $('#container').highcharts();

            tr.addClass('shown');
        }
    } );

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
    $('#ts-chart').hide()
    $('#stat_div').hide();
    $('#button').hide();


    // add the series to the chart
    var chart = $('#ts-chart').highcharts();


    addingseries();


    // change the app title
    document.title = 'Time Series Viewer';
    // force to adjust chart width when user hides or shows the side bar
    $("#app-content").on("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(event) {
        if (event.originalEvent.propertyName == 'padding-right') {
            $(window).resize(); // this forces the chart to redraw
        }
    });

})



/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    var chart1 = $('#container').highcharts();
    console.log(chart1);
    return '<object"><div id = "container" class ="highcharts-boxplot" style = "float:right"></div></object>'+
    '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+

                '<tr>'+
                    '<th></th>'+
                    '<th>hello</th>'+
                    '<th></th>'+
                '</tr>'+

        '<tr>'+
            '<td>Quality Control:</td>'+
            '<td>'+d.quality+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Method:</td>'+
            '<td>'+d.method+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Data Type:</td>'+
            '<td>'+ d.datatype+'</td>'+
        '</tr>'+
            '<tr>'+
            '<td>Value Type:</td>'+
            '<td>'+d.valuetype+'</td>'+
        '</tr>'+
            '<tr>'+
            '<td>Time Support:</td>'+
            '<td>'+d.timesupport+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Time Units:</td>'+
            '<td>'+d.timeunit+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Source Description:</td>'+
            '<td>'+d.sourcedescription+'</td>'+
        '</tr>'+
    '</table>';
}

function box () {
    $('#container').highcharts({

        chart: {
            type: 'boxplot'
        },

        title: {
            text: 'Highcharts box plot styling'
        },

        legend: {
            enabled: false
        },

        xAxis: {
            categories: ['1', '2', '3', '4', '5'],
            title: {
                text: 'Experiment No.'
            }
        },

        yAxis: {
            title: {
                text: 'Observations'
            }
        },

        plotOptions: {
            boxplot: {
                fillColor: '#F0F0E0',
                lineWidth: 2,
                medianColor: '#0C5DA5',
                medianWidth: 3,
                stemColor: '#A63400',
                stemDashStyle: 'dot',
                stemWidth: 1,
                whiskerColor: '#3D9200',
                whiskerLength: '20%',
                whiskerWidth: 3
            }
        },

        series: [{
            name: 'Observations',
            data: [
                [760, 801, 848, 895, 965]

            ]
        }]

    });
};
function finishloading(callback)
{
    $(window).resize();
    $('#ts-chart').show()
    $('#stat_div').show();
    $('#button').show();
    $(window).resize();
    $('#loading').hide();

}
function addingseries(callback){
     var res_id = find_query_parameter("res_id");
    var series_counter =0
     var chart = $('#ts-chart').highcharts();
     res_ids = res_id.split(",");
    for ( var r in res_ids)
    {
        series_counter = series_counter +1
    }

     for  (var  res_id in res_ids)
    {
        counter1.push(counter);
        add_series_to_chart(chart, res_ids[res_id],series_counter);

    };


}