function find_query_parameter(name) {
    url = location.href;
    //name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(url);
    return results == null ? null : results[1];
}
// here we set up the configuration of the CanvasJS chart
var data = [];
var unit_tracker = [];
var counter = 0;
var unit1 = null
var unit2 = null;
var resid_on = null;
counter1 = [];
var ymax =0
var ymin=0
var y2max=0
var y2min=0
// here we set up the configuration of the highCharts chart
var chart_options = {
    zoomEnabled: true,
    height: 600,
    legend: {
            cursor: "pointer",
            itemclick: function (e) {
                //console.log("legend click: " + e.dataPointIndex);
                //console.log(e);
                if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                    e.dataSeries.visible = false;
                } else {
                    e.dataSeries.visible = true;
                }

                e.chart.render();
            }
        },
    colorSet: 'greenShades',
    title: {
        fontSize: 20,
        text: "Data Series Viewer"
    },
    toolTip: {
        content: "{name}{y} <br>{x}"
    },
    data: [],
    axisX: {

        labelFontSize: 10
    },
    axisY: {
        fontSize: 15,
        labelFontSize: 10,
        titleWrap: true,
        titleMaxWidth: 150,
        gridThickness:2,
        includeZero: false,
        //viewportMaximum:180,
        //interval: 50
    },
    axisY2: {
        title: "test2",
        fontSize: 15,
        labelFontSize: 10,
        titleWrap: true,
        gridThickness:2,
        includeZero: false,
        //interval: 50
    }
};

// shows an error message in the chart title
function show_error(chart, error_message) {
    $('#loading').hide();
    console.log(error_message);
    $('#error-message').text(error_message);
}
var number2 = -1
var unit_list = [];
var title = 0
xtime = []
function add_series_to_chart(chart, res_id, number1, unit_off) {
    xtime.length = 0
    xval = ''
    yvalu = ''
    console.log(xtime)
    current_url = location.href;
    index = current_url.indexOf("timeseries-viewer");
    base_url = current_url.substring(0, index);
    var src = find_query_parameter("src");
    console.log(src)

    // in the start we show the loading...
    // the res_id can contain multiple IDs separated by comma
    if(src == "xmlrest"){
        res_id1 = 'test1'
    }
    else{
        res_id1 = res_id
    }


    console.log(res_id1)
    var csrf_token = getCookie('csrftoken');
    data_url = base_url + 'timeseries-viewer/chart_data/' + res_id1 + '/' + src + '/';
    $.ajax({
        type:"POST",
        headers:{'X-CSRFToken':csrf_token},
        dataType: 'json',
        data:{'url_xml':res_id},
        url: data_url,
        success: function (json) {
            // first of all check for the status
            var status = json.status;
            if (status !== 'success') {
                show_error(chart, "Error loading time series from " + res_id1 + ": " + status)
                $('#loading').hide();
                return;
            }
            // set the y axis title and units
            var units = json.units;
            if (units != null) {

                units = units.replace(/\s+/g, '');//removes any spaces in the units
            }
            if (units == null) {
                units = "N/A";
            }
            var unit_off_bool = false
            unit_tracker.push(units);//tracks the units of the different time series
            unit_different2 = null;
            same_unit = 1//goes to 2 when more than one unit type is graphed
            yaxis = 0 //tracks which dataset set goes on which axis
            var y_title = null;//tracks which variable to use for the yaxis title
            //data1 = json.for_canvas

            xval = json.xvalue
            yval = json.yvalue
            max1= json.max
            min1=json.min

            for (i=0;i<xval.length; i++)
            {
                //console.log("hello")
                temp_date = new Date(xval[i])
                xtime.push({x:temp_date.getTime(),y:yval[i]})
            }


            data1 = xtime

            var chart = $("#chartContainer").CanvasJSChart()
            //console.log(unit1)
            //console.log(units)
            //console.log(unit_off)
            if (unit_off == '') {
                unit1 = unit_tracker[0];
                if (unit1 == units) {
                    y_title = 0
                }
                if (unit1 != units)//checks the first unit type agaisnt the current unit
                {
                    same_unit = 2;//flags which axis is to be used
                    y_title = 1
                    if (unit2 == null) {
                        unit2 = units //this tracks the second unit type if there is one
                    }
                    if (units != unit2) {
                        same_unit = 3
                        y_title = 3
                    }
                }
            }
            else {
                y_title = 3
                unit_off_bool = true
                if (units != unit_off) {
                    if (units == unit1) {
                        y_title = 0
                        unit_off_bool = false
                    }
                    else if (resid_on == res_id) {
                        y_title = 1
                        unit_off_bool = false
                    }
                }
            }
            //// add the time series to the chart
            //series.data = json.for_highchart;
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
            if (site_name == null) {
                site_name = "N/A"
            }
            if (variable_name == null) {
                variable_name = "N/A"
            }
            if (organization == null) {
                organization = "N/A"
            }
            if (quality == null) {
                quality = "N/A"
            }
            if (method == null) {
                method = "N/A"
            }
            if (datatype == null) {
                datatype = "N/A"
            }
            if (valuetype == null) {
                valuetype = "N/A"
            }
            if(unit == null){
                unit='N/A'
            }

            if (timesupport == null) {
                timesupport = "N/A"
            }
            if (timeunit == null) {
                timeunit = "N/A"
            }
            if (sourcedescription == null) {
                sourcedescription = "N/A"
            }
            if (samplemedium == null) {
                samplemedium = "N/A"
            }
            number2 = number2 + 1//keeps track of row number for stats table
            number = number2;


            //max =200
            //min = 60
            if (y_title == 0) {//sets the y-axis title and flags that data should be plotted on this axis
                //chart.yAxis[0].setTitle({ text: json.variable_name + ' (' + json.units+')' });
                if( max > ymax){
                    ymax = max
                }
                console.log(ymin)
                console.log(min)
                if( min < ymin){
                    ymin = min
                }
                console.log(ymin)
                var newSeries =
                {
                    type: "line",
                    axisYType: "primary",
                    //axisYType:"secondary",
                    xValueType: "dateTime",
                    xValueFormatString:"MMM DD, YYYY: HH:mm",
                    showInLegend: false,
                    indexLabelFontSize: 1,
                    visible: true,
                    name: 'Site: ' + site_name + ' <br/> Variable: ' + json.variable_name + '<br/> Value: ',
                    dataPoints: data1
                };
                //console.log("data pushed 0 " + site_name)
                chart.options.axisY.title = json.variable_name + ' (' + json.units + ')'
                chart.options.axisY.titleWrap = true
                chart.options.data.push(newSeries);
                //maxview = Math.round(1000*(max+.1*max))/1000
                maxview = roundUp(Math.ceil(ymax))
                minview = roundDown(Math.floor(ymin))
                interval = (maxview-minview)/10
                console.log(maxview)
                console.log(minview)


                chart.options.axisY.viewportMaximum = maxview
                chart.options.axisY.maximum = maxview

                chart.options.axisY.viewportMinimum =  minview
                chart.options.axisY.minimum =  minview

                chart.options.axisY.interval = interval
            }
            else if (y_title == 1) {//sets the y-axis 2 title and flags that data should be plotted on this axis
                 if( max > y2max){
                    y2max = max
                }
                if( min < y2min){
                    y2min = min
                }
                var newSeries =
                {
                    type: "line",
                    //axisYType:"primary",
                    axisYType: "secondary",
                    xValueType: "dateTime",
                    xValueFormatString:"MMM DD, YYYY: HH:mm",
                    showInLegend: false,
                    indexLabelFontSize: 1,
                    visible: true,
                    name: 'Site: ' + site_name + ' <br/> Variable: ' + json.variable_name + '<br/> Value: ',
                    dataPoints: data1
                };
                //console.log("data pushed 1 " + site_name)
                chart.options.axisY2.title = json.variable_name + ' (' + json.units + ')'
                chart.options.axisY2.titleWrap = true
                chart.options.data.push(newSeries);
                //maxview = Math.round(1000*(max+.1*max))/1000


                maxview = roundUp(Math.ceil(y2max))
                minview = roundDown(Math.floor(y2min))
                console.log(maxview)
                console.log(minview)

                chart.options.axisY2.viewportMaximum = maxview
                chart.options.axisY2.viewportMinimum =  minview
                chart.options.axisY2.interval = ((maxview-minview)/10)
            }
            else if (y_title == 3) {//sets the y-axis 2 title and flags that data should be plotted on this axis
                var newSeries =
                {
                    type: "line",
                    //axisYType:"primary",
                    axisYType: "primary",
                    xValueType: "dateTime",
                    showInLegend: false,
                    indexLabelFontSize: 1,
                    visible: false,
                    name: 'Site: ' + site_name + ' <br/> Variable: ' + json.variable_name + '<br/> Value: ',
                    dataPoints: data1
                };
                chart.options.data.push(newSeries);
                console.log("data pushed 3 " + site_name)
            }
            //chart.options.axisX.title = "Number of points:"+count
            chart.options.axisY.titleFontSize = 15
            chart.options.axisY2.titleFontSize = 15
            chart.options.axisX.titleFontSize = 15

            //console.log(chart)
            //console.log(chart.options.axisY.viewportMaximum)
            //console.log(chart.options.axisY.viewportMinimum)
            //
            //console.log(chart.options.axisY.interval)
            //console.log(chart.options.axisY2.viewportMaximum)
            //console.log(chart.options.axisY2.viewportMinimum)
            //chart.options.axisY.viewportMaximum= 350
            //chart.options.axisY2.viewportMaximum = 330
            //chart.options.axisY2.interval = 11
            //console.log(chart.options.data )
            xtime = []

            if ((unit1 != units && unit2 != units) || unit_off_bool == true)//this triggers if more than 2 different units are used
            {
                var legend = "<div style='text-align:center'><input class = 'checkbox' id =" + number + " name =" + units + " data-resid =" + res_id
                    + " type='checkbox' onClick ='myFunc(this.id,this.name);' >" + "</div"
                $('#multiple_units').html("")
                $('#multiple_units').append('* Only two types of units are displayed at a time.');
                title = 1
                var chart = $("#chartContainer").CanvasJSChart()
            }
            else {
                //chart.setTitle({ text: "CUAHSI Data Series Viewer" });
                var legend = "<div style='text-align:center' '><input class = 'checkbox' id =" + number + " name =" + units + " data-resid =" + res_id
                    + " type='checkbox' onClick ='myFunc(this.id,this.name);'checked = 'checked'>" + "</div>"
                var chart = $("#chartContainer").CanvasJSChart()
            }
            var dataset = {
                legend: legend,
                organization: organization,
                name: site_name,
                variable: variable_name,
                unit: unit,
                samplemedium: samplemedium,
                count: count,//download:download,
                quality: quality,
                method: method,
                datatype: datatype,
                valuetype: valuetype,
                timesupport: timesupport,
                timeunit: timeunit,
                sourcedescription: sourcedescription,
                mean: mean,
                median: median,
                max: max,
                min: min,
                stdev: stdev,
                boxplot: boxplot,
                boxplot_count: boxplot_count
            }
            var table = $('#example').DataTable();
            table.row.add(dataset).draw();
            //end new table
            chart.render();
            if (number == number1 - 1)//checks to see if all the data is loaded before displaying
            {
                if (title == 1) {
                    //chart.setTitle({ text: "CUAHSI Data Series Viewer*" });
                    chart.options.title.text = "CUAHSI Data Series Viewer*"
                    chart.render();
                }
                else {
                    //chart.setTitle({ text: "CUAHSI Data Series Viewer" });
                    chart.options.title.text = "CUAHSI Data Series Viewer"
                    chart.render();
                }
                finishloading();
            }
        },
        error: function () {
            show_error("Error loading time series from " + res_id);
        }
    });
}
function roundUp(x){

    var negative = false;
    if(x < 0) {
        negative = true;
        x *= -1;
    } var y = Math.pow(10, x.toString().length-1);
    x = (x/y);
    x = Math.ceil(x);
    x = x*y;
    if(negative)
    {
        x *= -1;
    }
    return x;
}
function roundDown(x){
    //console.log(x)
    var negative = false;
    if(x<10 && x>=1){
        x = 0
        //console.log("hafasfsfsdf")
        return x
    }
    else if(x < 0) {
        if(x<0 &&x >= -10){
            x = -10
            return x
        }
        else{
            negative = true;
            x *= -1
        }
    }


    var y = Math.pow(10, x.toString().length-1);
    x = (x/y);
    x = Math.floor(x);
    x = x*y;

    //console.log(x)

    if(negative){
         x *= -1;
        //console.log(x)
        return x;
    }
    else{
        return x;
    }

}
var unit3 = ''
var res = null
function myFunc(id, name) {
    var chart1 = $("#chartContainer").CanvasJSChart()
    var number_chk = $('.checkbox').length
    var selected_box = document.getElementById(id)
    var check_unit = []
    var chk_unit = document.getElementById(id).name;
    var series = chart1.options.data[id].visible
    res = selected_box.getAttribute("data-resid")
    if (series == true) {
        chart1.options.data[id].visible = false
        chart1.render();
    } else if (series == false) {
        //first_unit =''
        if (chk_unit != unit1 && chk_unit != unit2) {
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
        else {
            chart1.options.data[id].visible = true
            chart1.render();
        }
    }
}

var popupDiv = $('#welcome-popup');
//end new table
$(document).ready(function (callback) {
    var res_id = find_query_parameter("res_id");
    var table = $('#example').DataTable({
        "createdRow": function (row, data, dataIndex) {
            color1 = null
            if (number == 0) {
                color1 = "#ec3131"
            }
            if (number == 1) {
                color1 = "#2cc52e"
            }
            if (number == 2) {
                color1 = "#fbfd07"
            }
            if (number == 3) {
                color1 = "#313eec"
            }
            if (number == 4) {
                color1 = "#dd25d5"
            }
            if (number == 5) {
                color1 = "#0d0c0d"
            }
            if (number == 6) {
                color1 = "#31cbec"
            }
            if (number == 7) {
                color1 = "#fb8915"
            }
            if (number == 8) {
                color1 = "#ffb8e7"
            }
            if (number == 9) {
                color1 = "#dd8585"
            }
            $('td', row).eq(0).css("backgroundColor", color1)
            $('td', row).eq(1).each(function () {
                var sTitle;
                sTitle = "Click here to see more data"
                this.setAttribute('title', sTitle);
            });

            var table = $('#example').DataTable()
            table.$('td').tooltip({
                selector: '[data-toggle="tooltip"]',
                container: 'body',
                "delay": 0,
                "track": true,
                "fade": 100
            });
        },
        data: data,
        "columns": [
            {
                "className": "legend",
                "data": "legend"
            },
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {"data": "organization"},
            {"data": "name"},
            {"data": "variable"},
            {"data": "unit"},
            {"data": "samplemedium"},
            {"data": "count"},
            //{"data":"download"}
        ],
        "order": [[1, 'asc']]
    });
    //Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(format(row.data())).show();
            box(row.data().boxplot_count);
            var series =
            {
                name: 'Site:' + row.data().name +
                ' Variable:' + row.data().variable,
                data: [],
                groupPadding: 0,
            }
            // add the time series to the chart
            series.data = [row.data().boxplot.map(Number)];
            var name_plot = '#container' + row.data().boxplot_count
            var chart = $(name_plot).highcharts();
            chart.setTitle({text: row.data().name});
            chart.yAxis[0].setTitle({text: row.data().variable + ' (' + row.data().unit + ')'})
            chart.xAxis[0].setTitle({
                text: 'Mean: ' + row.data().mean + ' Median: ' + row.data().median +'<br>'+
                ' Maximum: ' + row.data().max + '  Minimum : ' + row.data().min
            })
            chart.addSeries(series);
            tr.addClass('shown');
        }
    });
    if (res_id == null) {
        if (document.referrer == "https://apps.hydroshare.org/apps/") {
            $('#extra-buttons').append('<a class="btn btn-default btn" href="https://apps.hydroshare.org/apps/">Return to HydroShare Apps</a>');
        }
        popupDiv.modal('show');
    }http://r-fiddle.org/#/query/embed?code=
    $('#stat_div').hide();
    $('#button').hide();
    $('#loading').show();
    $('#multiple_units').hide();
    $('#example_length').html("")
    $('#example_filter').html("")
    $("#chart").toggle();
    // add the series to the chart
    addingseries();
    // change the app title
    document.title = 'Data Series Viewer';
})
/* Formatting function for row details - modify as you need */
function format(d) {
    // `d` is the original data object for the row
    name = 'container' + d.boxplot_count
    return '<div id = "container' + d.boxplot_count + '"class ="highcharts-boxplot" style = "float:right;height:300px;width:40%" ></div>' +
        '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:100px; margin-left:8.5%;font-size: 9pt">' +
        '<tr>' +
        '<td>Quality Control:</td>' +
        '<td>' + d.quality + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Method:</td>' +
        '<td>' + d.method + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Data Type:</td>' +
        '<td>' + d.datatype + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Value Type:</td>' +
        '<td>' + d.valuetype + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Time Support:</td>' +
        '<td>' + d.timesupport + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Time Units:</td>' +
        '<td>' + d.timeunit + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Source Description:</td>' +
        '<td>' + d.sourcedescription + '</td>' +
        '</tr>' +
        '</table>';
}

function box(number) {
    var name = '#container' + number
    $(name).highcharts({
        chart: {

            type: 'boxplot'
        },
        legend: {
            enabled: false
        },
        xAxis: {
            categories: 1,
            title: {
                text: ''
            },
            minRange: 1,
            labels: {enabled: false}
        },
        yAxis: {
            labels: {
                style: {
                    width: '20px'
                },
                step: 1
            }
        },
        title: {
            align: 'center'
        },
        plotOptions: {
            series: {
                groupPadding: 0
            }
        },
    });
};
function finishloading(callback) {
    $(window).resize()
    $('#stat_div').show();
    $(window).resize();
    $('#loading').hide();
    $('#multiple_units').show();
    var chart = $("#chartContainer").CanvasJSChart()
    $("#chart").toggle();
    chart.render();
    console.log(Date())

}
function addingseries(unit_off) {
    var res_id = find_query_parameter("res_id");
    var series_counter = 0
    if (unit_off == null) {
        unit_off = ''
    }
    if (res_id != null) {
        res_ids = res_id.split(",");
    }
    else {
        res_ids = ''
        $('#loading').hide();
    }
    for (var r in res_ids) {
        series_counter = series_counter + 1
    }
    CanvasJS.addColorSet("greenShades",
        [//colorSet Array
            "#ec3131",
            "#2cc52e",
            "#fbfd07",
            "#313eec",
            "#dd25d5",
            "#0d0c0d",
            "#31cbec",
            "#fb8915",
            "#ffb8e7",
            "#dd8585",

        ])
    $("#chartContainer").CanvasJSChart(chart_options);
    var chart = $("#chartContainer").CanvasJSChart()
    counter2 = 0
    for (var res_id in res_ids) {
        xtime = []
        counter1.push(counter);
        add_series_to_chart(chart, res_ids[res_id], series_counter, unit_off);
        counter2 = counter2 + 1
    }
}
function multipletime() {
    var popupDiv = $('#hello');
    var chart = $("#chartContainer").CanvasJSChart()
    popupDiv.modal('hide');
    $('#stat_div').hide();
    $('#multiple_units').hide();
    $('#loading').show();
    var unit_off = document.querySelector('input[name = "units"]:checked').value;
    unit1 = document.querySelector('input[name = "units"]:not(:checked)').value;
    unit2 = unit3
    resid_on = res
    chart.options.data = []
    chart.render()
    $("#chart").toggle();
    ymax =0
    ymin=0
    y2max=0
    y2min=0
    var table = $('#example').DataTable();
    number2 = -1
    table
        .clear()
        .draw();
    addingseries(unit_off);
}

$('#reset').on('click', function () {
    var chart = $("#chartContainer").CanvasJSChart()
    chart.options.data = []
    chart.render()
})
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
