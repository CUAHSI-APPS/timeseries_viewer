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
var unit1=null
var unit2=null;
var resid_on = null;
counter1 =[];
// here we set up the configuration of the highCharts chart
Highcharts.setOptions({
    plotOptions: {
        //area: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //arearange: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //areaspline: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //areasplinerange: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //bar: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //boxplot: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //bubble: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //column: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //columnrange: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //errorbar: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //funnel: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //gauge: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //heatmap: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //line: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //pie: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //polygon: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //pyramid: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //scatter: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //series: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //solidgauge: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //spline: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //treemap: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
        //waterfall: { animation: false, enableMouseTracking: false, stickyTracking: true, shadow: false, dataLabels: { style: { textShadow: false } } },
    }
    //chart: {
//        //reflow: false,
//        //events: {
//        //    redraw: function() {
//        //        console.log("highcharts redraw, rendering-done");
//        //        $('body').addClass('rendering-done');
//        //    }
//        //},
//        //animation: false
//    },
//    tooltip: {
//        enabled: true,
//        animation: true
//    },
//    exporting: {
//        enabled:false
//    },
//    credits: {
//        enabled: false
//    }
//});
//var chartData={
//    "type":"line",
//    "legend":{
//
//  },
//    "title":{
//        "text": "Time Series Viewer"
//    },
//
//    "scale-x":{
//
//        "transform":{
//                    "type":"date",
//                    "all":"%M-%Y",
//            "item":{"visible":false}
//    }},
//    "scale-y":{
//        //"line-color":"#29A2CC",
//        "label":{
//          "text":""
//        }
//    },
//    "scale-y-2":{ /*you must associate your data to the correct scale when using multiple scales*/
//        //"line-color":"#D31E1E",
//
//        "label":{
//            "text":""
//    }
//},
//
//    "series":[
//
//    ]
  });
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
                    color: Highcharts.getOptions().colors[1],
                        fontSize:'15px'
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
                    color: Highcharts.getOptions().colors[1],
                    fontSize:'15px'
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
    //var button = chart.exportSVGElements[0];
   // button.destroy();
     $('#loading').hide();
    console.log(error_message);
    //$('#ts-chart').show()
    $('#error-message').text(error_message);
    //chart.setTitle({ text: "" });
}

var number2 = -1
var unit_list =[];
function add_series_to_chart(chart,res_id,number1,unit_off) {
    current_url = location.href;
    index = current_url.indexOf("timeseries-viewer");
    base_url = current_url.substring(0, index);
    // in the start we show the loading...
    // the res_id can contain multiple IDs separated by comma
    console.log(unit_off)
    data_url = base_url + 'timeseries-viewer/chart_data/' + res_id + '/';
    $.ajax({
        url: data_url,
        success: function(json) {
            // first of all check for the status
            var status = json.status;
            if (status !== 'success') {
                show_error(chart, "Error loading time series from " + res_id + ": " + status)
                $('#loading').hide();
                return;
            }
               // set the y axis title and units
            var units = json.units;
            units  = units.replace(/\s+/g, '');//removes any spaces in the units
            if(units==null) {
                units = "";
            }

             var unit_off_bool = false
            unit_tracker.push(units);//tracks the units of the different time series
            //console.log(unit_tracker)

            unit_different2=null;
            same_unit = 1//goes to 2 when more than one unit type is graphed
            yaxis=0 //tracks which dataset set goes on which axis
            var y_title = 0;//tracks which variable to use for the yaxis title
            console.log(unit_off)
            console.log(units)

            if(unit_off == ''){
                unit1 = unit_tracker[0];
                if (unit1 !=units)//checks the first unit type agaisnt the current unit
                {
                  same_unit = 2;//flags which axis is to be used
                    y_title = 1
                  if(unit2 == null)
                  {
                      unit2 =units //this tracks the second unit type if there is one


                  }
                    if(units != unit2){
                        same_unit = 3
                        y_title = 3
                    }
                 };

                }

            else{
                if(units != unit_off){
                    if(units ==unit1){
                        yaxis = 0
                        y_title = 0
                    }
                    else if(resid_on == res_id){
                        yaxis = 1
                        y_title =1

                    }
                    else{
                        unit_off_bool = true
                        same_unit =2
                        y_title = 3
                    }

                }


            }


            //console.log(unit1)
            //console.log(unit_different1)
            //console.log(yaxis)



            if (same_unit == 2 )
            {

                yaxis = 1;
            }
            console.log(yaxis)


            //
            var series =
            {
                id: res_id,
                name:  'Site: '+json.site_name
                +'. Variable: ' + json.variable_name,
                data: [],
                yAxis: yaxis,

            }
            //
            //// add the time series to the chart
            series.data = json.for_highchart;
            //
            //
            //
            chart.addSeries(series);
            ////console.log(json.smallest_value)



            //values1 = json.for_highchart;
            //var scales =''
            console.log(units)
            if (y_title ==0){//sets the y-axis title and flags that data should be plotted on this axis

                chart.yAxis[0].setTitle({ text: json.variable_name + ' (' + json.units+')' });

                //zingchart.exec('chartDiv', 'modify', {
                //data: {
                //    scaleY: {
                //        label: {
                //            text: json.variable_name + ' (' + units+')',
                //            fontSize: "10px"
                //        }
                //    }
                //}
                //});
                //scales1 = "scale-x,scale-y"
                //
                //zingchart.exec('chartDiv', 'addplot', {
                //        data :
                //            {
                //                values : values1,
                //                scales: scales1
                //            }
                //        });
            }
            else if(y_title ==1){//sets the y-axis 2 title and flags that data should be plotted on this axis

                chart.yAxis[1].setTitle({text: json.variable_name + ' (' + json.units+')'})
                //zingchart.exec('chartDiv', 'modify', {
                //data: {
                //    "scale-y-2": {
                //        label: {
                //            text: json.variable_name + ' (' + units+')',
                //            fontSize: "10px",
                //            lineColor:"#29A2CC",
                //        }
                //    }
                //}
                //});
                //scales1 = "scale-x,scale-y-2"
                // zingchart.exec('chartDiv', 'addplot', {
                //        data :
                //            {
                //                values : values1,
                //                scales: scales1
                //            }
                //        });

            }



            //// now we can hide the loading... indicator
            ////chart.hideLoading();
            chart.legend.group.hide();
            //// if we have values more than threshold, show title
            //if (json.count >= 50000) {
            //    chart.setTitle({text: 'Showing first 50000 values'})
            //}

            // set the metadata elements content
            //var metadata_info =
             //
             //"<b>Site: </b>"+site_name +"<br>"+
             //"<b>Variable: </b>"+variable_name+","+ datatype+","+valuetype +"<br>"+
             //"<b>Organization: </b>"+organization +"<br>"+
             //"<b>Quality: </b>"+quality +"<br>"+
             //"<b>Method: </b>"+method +"<br>"+
             //"<b>Sample Medium: </b>"+samplemedium+"<br>"

            //$('#metadata').append(metadata_info);
            //$('#metadata_test1').append(metadata_info);
            //$('#metadata-loading').hide();

            // add the row to the statistics table
            number2 = number2+1//keeps track of row number for stats table
            number  = number2;
            //var stats_info = "<tr>" +
            //"<td style='text-align:center' bgcolor = "+chart.series[number].color+"><input id ="+number
            //    + " type='checkbox'onClick ='myFunc(this.id);'checked = 'checked'>" + "</td>" +
            //"<td>" + json.site_name + "</td>" +
            //"<td>" + variable_name+", "+ datatype+", "+valuetype  + "</td>" +
            //"<td>" + organization + "</td>" +
            //"<td>" + quality + "</td>" +
            //"<td>" + method + "</td>" +
            //"<td>" + samplemedium + "</td>" +
            //"<td>" + json.count + "</td>" +
            //"<td>" + json.mean + "</td>" +
            //"<td>" + json.median + "</td>" +
            //"<td>" + json.stdev.toFixed(4) + "</td></tr>";
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
            var max = json.max
            var min = json.min
            var stdev = json.stdev
            var timesupport = json.timesupport
            var timeunit = json.timeunit
            var sourcedescription = json.sourcedescription
            var boxplot_count = number2
            var boxplot = json.boxplot
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

            //$("#chartDiv").minimizeLegend();

        //    $("#chartDiv").hidePlot({
        //        plotindex:number
        //});


        console.log(units)
            console.log(unit)


            //hideplot(0);

            //$("#chartDiv").hideAllPlots();
            //var download = '<a href = "http://google.com"  class="btn btn-primary">CSV</a>'+
            //        '<a href = "http://bcc-hiswebclient.azurewebsites.net/CUAHSI/HydroClient/WaterOneFlowArchive/'+res_id+'/zip" class="btn btn-info">Water ML </a>'
            //this section checks to see if more than two units are displayed. If true it will not display the data after the first two sets of units
            if((unit1 != units && unit2 !=units)|| unit_off_bool == true  )//this triggers if more than 2 different units are used
            {
                //chart.hideLoading();
                //$('#metadata-loading').hide();
                //chart.destroy();
                //$("#stats-table").hide();
                //$("#metadata-list").hide();
                //$('#error-message').text("Error loading time series "+ res_id+". More than two unit types detected.");
                //return;
                var legend = "<div style='text-align:center'><input class = 'checkbox' id ="+number+" name ="+ units+" data-resid ="+res_id
                + " type='checkbox' onClick ='myFunc(this.id,this.name);' >" + "</div"
                var series = chart.series[number];
                if (series.visible) {
                    series.hide();
                }

                $('#multiple_units').html("")
                $('#multiple_units').append('* Only two types of units are displayed at a time.');
                 chart.setTitle({ text: "CUAHSI Time Series Viewer*" });
            }
            else{
                 chart.setTitle({ text: "CUAHSI Time Series Viewer" });
                var legend = "<div style='text-align:center' '><input class = 'checkbox' id ="+number+" name ="+ units+" data-resid ="+res_id
                + " type='checkbox' onClick ='myFunc(this.id,this.name);'checked = 'checked'>" + "</div>"
            }
            var dataset = {legend:legend,organization:organization,name:site_name,variable:variable_name,unit:unit,samplemedium:samplemedium,count:count,//download:download,
                quality:quality,method:method,datatype:datatype,valuetype:valuetype, timesupport:timesupport,timeunit:timeunit,
                sourcedescription:sourcedescription,
                mean:mean,median:median,max:max,min:min,stdev:stdev,boxplot:boxplot,boxplot_count:boxplot_count}
            var table = $('#example').DataTable();
            table.row.add(dataset).draw();


            //end new table

            if (number == number1-1)//checks to see if all the data is loaded before displaying
            {
                $(window).resize();
                finishloading();

            }


            $(window).resize();//This fixes an error where the grid lines are misdrawn when legend layout is set to vertical
        },
        error: function() {
            show_error("Error loading time series from " + res_id);
        }
    });

}
var unit3 =''
var res = null
function myFunc(id,name)
{
    //var check = document.getElementById(id).checked
    //if(check == false)
    //{
    //   zingchart.exec('chartDiv', 'hideplot', {
    //    plotindex : id
    //    });
    //}
    //if(check == true)
    //{
    //    zingchart.exec('chartDiv', 'showplot', {
    //        plotindex: id
    //    });
    //}
    var chart1 = $('#ts-chart').highcharts();
    var number_chk = $('.checkbox').length
    var selected_box = document.getElementById(id)
    var check_unit=[]

    var chk_unit = document.getElementById(id).name;

    var series = chart1.series[id];
    res = selected_box.getAttribute("data-resid")

    console.log(res);
    console.log(chk_unit)
    console.log(unit1)
    console.log(unit2)
        if (series.visible ==true) {
            series.hide();
        } else if (series.visible == false){
            //first_unit =''
            if (chk_unit != unit1 && chk_unit != unit2) {

                //for(i =0; i<=number_chk; i++) {
                //
                //    if ($('#' + i).is(':checked')) {
                //        //console.log("checked")
                //        var unit_name = $('#' + i).attr('name')
                //        if (i == 0) {
                //            check_unit.push(unit_name)
                //            first_unit = unit_name
                //        }
                //        else if (first_unit != unit_name) {
                //            check_unit.push(unit_name)
                //        }
                //
                //    }
                //}
                var test1 = 'Please select a unit type to hide.<br>' +
                    '<input type="radio" id ="r1" name ="units" value=' + unit1 + ' checked>' + unit1 + '<br>' +
                    '<input type="radio" id ="r2" name ="units" value=' + unit2 + '>' + unit2 + '<br>' +
                    '<button class="btn btn-danger" id="change_unit" onclick ="multipletime()" >submit</button>'
                $('#' + id).attr('checked', false);
                $('#hello2').html("")
                $('#hello2').append(test1)

                unit3 = chk_unit
                var popupDiv = $('#hello');
                popupDiv.modal('show');
                check_unit.length = 0;
            }
            else
            {
                series.show();
            }

        }

    //console.log(check_unit)
    //var chart1 = $('#ts-chart').highcharts();
    //var series = chart1.series[id];
    //    if (series.visible) {
    //        series.hide();
    //    } else {
    //        series.show();
    //    }
    //
    //
    //for(var i = 0; i< unit_list.length; i++)
    //{
    //    console.log(unit_list[i][1])
    //}

}


var popupDiv = $('#welcome-popup');
    //end new table
$(document).ready(function (callback) {
    var res_id = find_query_parameter("res_id");

    //var chart =$('#chartDiv').zingchart({data:chartData})
    var table = $('#example').DataTable( {
        "createdRow":function(row,data,dataIndex)
        {
            var chart = $('#ts-chart').highcharts();
            //console.log("created")
            $('td',row).eq(0).css("backgroundColor", chart.series[number].color)
             $('td',row).eq(1).each( function()
             {
                var sTitle;
                sTitle = "Click here to see more data"
                this.setAttribute( 'title', sTitle );
                } );
                //$('#example tbody tr').setAttribute( 'title', 'hi' );
                //$('td'.row).setAttribute('title',"hello");
                 /* Apply the tooltips */

                var table = $('#example').DataTable()
                table.$('td').tooltip( {
                     selector: '[data-toggle="tooltip"]',
                    container: 'body',
                    "delay": 0,
                    "track": true,
                    "fade": 100
            } );


        },

        //"fnCreatedRow":function(nRow,aData, iDataIndex){
        //    //var plot_attr = zingchart.exec('chartDiv', 'getobjectinfo', {
        //    //object : 'plot'
        // });
        //    var line_color = plot_attr.lineColor
            //$('td',nRow).eq(0).css("backgroundColor", line_color);

         //   var plot_attr = zingchart.exec('chartDiv', 'getscales', {
         //   object : 'plot'
         //});

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
            { "data": "count" },

            //{"data":"download"}
            ],
        "order": [[1, 'asc']]
    } );
    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() )
        {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else
        {
            // Open this row

            row.child( format(row.data()) ).show();
            box(row.data().boxplot_count);
            var series =
            {
                name:  'Site:'+row.data().name+
                ' Variable:'+row.data().variable,
                data: [],
                groupPadding:0,
            }
            // add the time series to the chart
            series.data = [row.data().boxplot.map(Number)];

            var name_plot = '#container'+row.data().boxplot_count

            var chart = $(name_plot).highcharts();
            chart.setTitle({ text: row.data().name });
            chart.yAxis[0].setTitle({ text: row.data().variable + ' (' + row.data().unit+')' })
            chart.xAxis[0].setTitle({text:'Mean: '+row.data().mean +' Median: '+row.data().median+
            ' Maximum: '+row.data().max +'  Minimum : '+row.data().min})

            chart.addSeries(series);
            //chart.renderer.label('Mean: '+row.data().mean +' Median: '+row.data().median, 240, 232,0,0,true)
            //    .css({
            //
            //        fontSize: '12px'
            //    })
            //    .add();
            tr.addClass('shown');
        }
    } );

    //$('#example tbody tr').each( function() {
    //    sTitle = "hello";
    //    this.setAttribute( 'title', sTitle );
    //} );

    if (res_id == null) {
        if (document.referrer == "https://apps.hydroshare.org/apps/") {
            $('#extra-buttons').append('<a class="btn btn-default btn" href="https://apps.hydroshare.org/apps/">Return to HydroShare Apps</a>');
        }
        popupDiv.modal('show');
    }

    //// initialize the chart and set chart height


    //$('#chartDiv').hide();
    $('#ts-chart').hide()
    $('#stat_div').hide();
    $('#button').hide();
    $('#loading').show();
    $('#multiple_units').hide();
     $('#example_length').html("")
    $('#example_filter').html("")


    // add the series to the chart
    addingseries();
    //hideplot(0);

    // change the app title
    document.title = 'Time Series Viewer';
    // force to adjust chart width when user hides or shows the side bar
    //$("#app-content").on("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(event) {
    //    if (event.originalEvent.propertyName == 'padding-right') {
    //        //$(window).resize(); // this forces the chart to redraw
    //    }
    //});
    //$("#chartDiv").hideAllPlots();

})



/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row

    name ='container'+ d.boxplot_count


    return '<div id = "container'+ d.boxplot_count+'"class ="highcharts-boxplot" style = "float:right;height:250px;width:40%" ></div>'+

    '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:100px; margin-left:8.5%;font-size: 9pt">'+

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
        '<tr>'+
            '<td>Mean:</td>'+
            '<td>'+d.mean+'</td>'+
        '</tr>'+
            '<tr>'+
            '<td>Median:</td>'+
            '<td>'+d.median+'</td>'+
        '</tr>'+
    '</table>';
}

function box (number) {
    var name = '#container'+number

    $(name).highcharts({

        chart: {

            type: 'boxplot'
        },
        legend:{
            enabled:false
        },
        xAxis: {
            categories: 1,
            title:{
                text:''
            },
            minRange: 1,
            labels:{enabled:false}

        },
        title:{
            align: 'center'
        },
        plotOptions: {
            series: {
                groupPadding: 0
            }
        },


    });
};
function finishloading(callback)
{
    $(window).resize();


    //$('#button').show();
    $('#stat_div').show();
    $('#ts-chart').show();
    $(window).resize();
    $('#loading').hide();
    $('#multiple_units').show();


}
function addingseries(unit_off){
     var res_id = find_query_parameter("res_id");
     var series_counter =0

    var page_height = $(document).height();
      var page_width = $(document).width();
    if (page_height > 500) {
        height1 = page_height - 225;
    }


    var page_height = $(document).height();
    if (page_height > 500) {
        chart_options.chart.height = page_height - 225;
    }
    console.log("highchart")
    $('#ts-chart').highcharts(chart_options);

    // Render Method[2]
    //  chart = zingchart.render({
    //  id:'chartDiv',
    //  output:"svg",
    //  data:chartData,
    //  height:height1,
    //  width: '100%'
    //
    //});


     var chart = $('#ts-chart').highcharts();

    if (unit_off == null){
        unit_off = ''
    }
    console.log(unit_off)
     if (res_id != null)
	{
     	res_ids = res_id.split(",");
	}
	else
     {
        res_ids =''
         $('#loading').hide();
     }
    for ( var r in res_ids)
    {
        series_counter = series_counter +1
    }
    counter2 = 0
     for  (var  res_id in res_ids)
    {
        counter1.push(counter);

        add_series_to_chart(chart,res_ids[res_id],series_counter,unit_off); //highchart
        //add_series_to_chart1(chart, res_ids[res_id],series_counter); //zing chart
        counter2 = counter2+1
        //console.log(counter2)
    };



}
function dtime(ref){
    var time = new Date();

}
function multipletime()
{
    var popupDiv = $('#hello');
    popupDiv.modal('hide');
    $('#stat_div').hide();
    $('#ts-chart').hide();
    $('#multiple_units').hide();
    $('#loading').show();
    var unit_off = document.querySelector('input[name = "units"]:checked').value;
    unit1 = document.querySelector('input[name = "units"]:not(:checked)').value;
    unit2 = unit3
    resid_on = res
    $('#ts-chart').highcharts().destroy();
    var table = $('#example').DataTable();
    number2 = -1
    table
    .clear()
    .draw();
    addingseries(unit_off);

}


  //window.onload=function(){
  //   var page_height = $(document).height();
  //    var page_width = $(document).width();
  //  if (page_height > 500) {
  //      height1 = page_height - 225;
  //  }
  //  // Render Method[2]
  //    chart = zingchart.render({
  //    id:'chartDiv',
  //    output:"svg",
  //    data:chartData,
  //    height:height1,
  //        width: 1200
  //
  //  });
  //};
//function hideplot(index){
//    console.log('hide plot')
//    console.log(index)
//    zingchart.exec('chartDiv', 'hideplot', {
//                plotindex : index
//                });
//
//}
// $(function () {
//        $("example").tooltip({
//            selector: '[data-toggle="tooltip"]',
//            container: 'body'
//        });
//    })