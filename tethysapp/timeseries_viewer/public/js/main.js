var data = [];
var unit_tracker = [];
var unit1 = null
var unit2 = null;
var resid_on = null;
//ymax and ymin store the maximum y value for each axis.
var ymax =0
var ymin=0
var y2max=0
var y2min=0
//tool tip for the quality control column
var quality_title=null
var number = 0
var counter_all =0
var end_of_resources = 0
var unit3 = ''
var res = null
// here we set up the configuration of the CanvasJS chart
// 269 maximally distinct colors
var color_selection = [ "#FF4A46", "#008941", "#006FA6", "#A30059","#000000", "#FFFF00", "#1CE6FF", "#FF34FF",
        "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
        "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
        "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
        "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
        "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
        "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
        "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",

        "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
        "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
        "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
        "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
        "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
        "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
        "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
        "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58",

        "#7A7BFF", "#D68E01", "#353339", "#78AFA1", "#FEB2C6", "#75797C", "#837393", "#943A4D",
        "#B5F4FF", "#D2DCD5", "#9556BD", "#6A714A", "#001325", "#02525F", "#0AA3F7", "#E98176",
        "#DBD5DD", "#5EBCD1", "#3D4F44", "#7E6405", "#02684E", "#962B75", "#8D8546", "#9695C5",
        "#E773CE", "#D86A78", "#3E89BE", "#CA834E", "#518A87", "#5B113C", "#55813B", "#E704C4",
        "#00005F", "#A97399", "#4B8160", "#59738A", "#FF5DA7", "#F7C9BF", "#643127", "#513A01",
        "#6B94AA", "#51A058", "#A45B02", "#1D1702", "#E20027", "#E7AB63", "#4C6001", "#9C6966",
        "#64547B", "#97979E", "#006A66", "#391406", "#F4D749", "#0045D2", "#006C31", "#DDB6D0",
        "#7C6571", "#9FB2A4", "#00D891", "#15A08A", "#BC65E9", "#FFFFFE", "#C6DC99", "#203B3C",

        "#671190", "#6B3A64", "#F5E1FF", "#FFA0F2", "#CCAA35", "#374527", "#8BB400", "#797868",
        "#C6005A", "#3B000A", "#C86240", "#29607C", "#402334", "#7D5A44", "#CCB87C", "#B88183",
        "#AA5199", "#B5D6C3", "#A38469", "#9F94F0", "#A74571", "#B894A6", "#71BB8C", "#00B433",
        "#789EC9", "#6D80BA", "#953F00", "#5EFF03", "#E4FFFC", "#1BE177", "#BCB1E5", "#76912F",
        "#003109", "#0060CD", "#D20096", "#895563", "#29201D", "#5B3213", "#A76F42", "#89412E",
        "#1A3A2A", "#494B5A", "#A88C85", "#F4ABAA", "#A3F3AB", "#00C6C8", "#EA8B66", "#958A9F",
        "#BDC9D2", "#9FA064", "#BE4700", "#658188", "#83A485", "#453C23", "#47675D", "#3A3F00",
        "#061203", "#DFFB71", "#868E7E", "#98D058", "#6C8F7D", "#D7BFC2", "#3C3E6E", "#D83D66",

        "#2F5D9B", "#6C5E46", "#D25B88", "#5B656C", "#00B57F", "#545C46", "#866097", "#365D25",
        "#252F99", "#00CCFF", "#674E60", "#FC009C", "#92896B"]
var chart_options = {
    zoomEnabled: true,
    height: 600,
    // exportEnabled: true,
    legend: {
        cursor: "pointer",
        itemclick: function (e) {
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
        title: "",
        fontSize: 15,
        labelFontSize: 10,
        titleWrap: true,
        //gridThickness:2,
        gridThickness:0,
        includeZero: false,
    }
};
var popupDiv = $('#welcome-popup');
var series_tracker = []
var row_tracker = []
var hs_res_list_loaded = false
var add_hs_res = []

$(document).ready(function (callback) {
    // document.getElementById('screenshot').addEventListener('click', function() {
    //     downloadCanvas(this);
    // }, false);

    console.log("ready")
    // var src = find_query_parameter("SourceId");
    // var wu = find_query_parameter("WofUri");
    // var source =find_query_parameter("Source");
    // if (source[0] == "cuahsi"){
    //     src='cuahsi'
    // }
    // else{
    //     var src1 = find_query_parameter("src");
    //
    //     if (src1 =='hydroshare'){src = src1}
    //     else if (src1 =='xmlrest'){src=src1}
    //     else{src =null}
    // }

    var table = $('#data_table').DataTable({
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],

        "createdRow": function (row, data, dataIndex) {
            var col_counter = 0
            columns =
            this.api().columns().every( function () {
                if (col_counter >1){

                    var column = this;
                    var select = $('<select style="width: 100% !important;"><option value="" selected >Show All: '+this.title()+'</option></select>')
                        .appendTo( $(column.footer()).empty() )
                        .on( 'change', function () {
                            var val = $.fn.dataTable.util.escapeRegex(
                                $(this).val()
                            );

                            column
                                .search( val ? '^'+val+'$' : '', true, false )
                                .draw();
                        } );

                    column.data().unique().sort().each( function ( d, j ) {
                        select.append( '<option value="'+d+'">'+d+'</option>' )
                    } );
                }

                col_counter = col_counter +1
            } );

            color1 = color_selection[dataIndex]
            $('td', row).eq(0).css("backgroundColor", color1)
            $('td', row).eq(1).each(function () {
                var sTitle;
                sTitle = "Click here to see more data"
                this.setAttribute('title', sTitle);
            });
            $('td', row).eq(6).each(function () {
                ;
                sTitle = {"data": "quality"},
                    this.setAttribute('title', quality_title);
            });
            //console.log({"data": "quality"})
            var table = $('#data_table').DataTable()
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
                "name":"legend",
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
            {"data": "quality"},
            {"data": "count"},
            //{"data":"download"}
        ],
        "order": [[1, 'asc']]
    });

    //Add event listener for opening and closing details
    $('#data_table tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        row_num = row[0][0]
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
            // creating and formatting the boxplot for each time series
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


    $('#hs_resource_table').DataTable({
        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        "scrollY":true,
        "createdRow": function (row, data, dataIndex) {
            var col_counter = 0
            columns =
            this.api().columns().every( function () {
                if (col_counter >1){

                    var column = this;
                    var select = $('<select style="width: 100% !important;"><option value="" selected >Show All: '+this.title()+'</option></select>')
                        .appendTo( $(column.footer()).empty() )
                        .on( 'change', function () {
                            var val = $.fn.dataTable.util.escapeRegex(
                                $(this).val()
                            );

                            column
                                .search( val ? '^'+val+'$' : '', true, false )
                                .draw();
                        } );

                    column.data().unique().sort().each( function ( d, j ) {
                        select.append( '<option value="'+d+'">'+d+'</option>' )
                    } );
                }

                col_counter = col_counter +1
            } );

            // color1 = color_selection[dataIndex]
            // $('td', row).eq(0).css("backgroundColor", color1)
            // $('td', row).eq(1).each(function () {
            //     var sTitle;
            //     sTitle = "Click here to see more data"
            //     this.setAttribute('title', sTitle);
            // });
            // $('td', row).eq(6).each(function () {
            //     ;
            //     sTitle = {"data": "quality"},
            //         this.setAttribute('title', quality_title);
            // });
            //console.log({"data": "quality"})
            var table = $('#hs_resource_table').DataTable()
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
                "name":"legend",
                "className": "legend",
                "data": "legend"
            },
            {"data": "title"},
            {"data": "type"},
            {"data": "author"},
            {"data": "update"},
            //{"data":"download"}
        ],
        "order": [[1, 'asc']]
    });
    document.title = 'Data Series Viewer';
    $('#loading').show();
    $("#chart").hide();
    $('#stat_div').hide();
    $('#multiple_units').hide();
    $("#modalLoadRes").on("show.bs.modal", function () {
    // Set delay so that resize function will trigger properly
        loadMap();
        setTimeout(function(){
            console.log('resize')
            $(window).trigger("resize");
        }, 500);
    });

    addingseries();
    //$('#button').hide();


    //$('#data_table_length').html("")
    //$('#data_table_filter').html("")

    // change the app title

})

function addingseries(unit_off) {
    var src = find_query_parameter("src");
    var series_counter =0
    var source = find_query_parameter('Source')
    console.log(source)
    // var end_of_resources = false
    var chart = $("#chartContainer").CanvasJSChart()
    var counter = 0
    var res_id =null
    var xml_rest_id=null
    var sources = []
    CanvasJS.addColorSet("greenShades",color_selection)
    $("#chartContainer").CanvasJSChart(chart_options);
    //
    // if (source[0] == 'cuahsi'){
    //     src='cuahsi'
    // }
    // else if (source[0]=''){window.location ='http://data.cuahsi.org/#'}

    if (source[0] =='cuahsi'){
        console.log('cuahsi')
        src = source[0]
        res_id=find_query_parameter('WofUri')
        var quality=find_query_parameter('QCLID')
        var method=find_query_parameter('MethodId')
        var sourceid = find_query_parameter('SourceId')
    }
    else if(src=='hydroshare') {
        res_id = find_query_parameter("res_id");
    }
    else if (src=='xmlrest'){
        res_id = find_query_parameter("res_id");
        res_id = res_id[0].split(',')
        xml_rest_id = res_id
        res_id ='xmlrest'
    }

    if (unit_off == null) {
        unit_off = ''
    }
    //Create an array of same dimension of res_id with sources
    sources = res_id.slice()
    sources = sources.fill(src)
    //Add selected hs resources to resource list
    res_id =res_id.concat(add_hs_res)

    end_of_resources = res_id.length
    console.log(series_counter)
    console.log('@@@@@@@@@@@@@@@@@@@@@@@')


    for (var id in res_id){
        src = sources[id]
        if (src == undefined){
            src = 'hydroshare'
        }
        // Checking filter parameters from CUAHSI
        if( src =='cuahsi'){
            if(quality[id]=='null' || quality[id]=='None')
            {quality1=''}
            else{quality1 = quality[id]}
            if(method[id]=='null' || method[id]=='None')
            {method1=''}
            else{method1 = method[id]}
            if(sourceid[id]=='null' ||sourceid[id]=='None')
            {sourceid1=''}
            else{sourceid1 = sourceid[id]}
            id_qms =  quality1 +'aa'+method1+'aa'+sourceid1
        }
        else{
            id_qms="not_cuahsi"
        }
        counter = counter + 1
        // if (counter ==series_counter){end_of_resources =true}
        // add_series_to_chart(chart, res_id[id], end_of_resources, unit_off,id_qms,src);

        length_master= 0
        var current_url = location.href;
        var index = current_url.indexOf("timeseries-viewer");
        var base_url = current_url.substring(0, index);
        var csrf_token = getCookie('csrftoken');
        var data_url = base_url + 'timeseries-viewer/chart_data/' + res_id[id] + '/' + src + '/';
        var res_id_counter = 0
        $.ajax({
            type:"POST",
            headers:{'X-CSRFToken':csrf_token},
            dataType: 'json',
            data:{'url_xml':xml_rest_id},
            url: data_url,
            success: function (json) {
                var dseries =[]
                console.log(json)
                error = json.error
                if (error != ''){show_error(error)}
                else {
                    var chart = $("#chartContainer").CanvasJSChart()
                    json = json.data
                    console.log(json)
                    console.log(res_id.length)
                    var json_len = json.length
                    end_of_resources = end_of_resources + json_len -1
                    for (series in json) {
                        //number of res_ids


                        console.log('start series')
                        // if (res_id_counter == series_length){
                        //     end_of_data = true
                        // }
                        plot_data(chart, res_id[id], series_counter, unit_off, id_qms, json[series])
                        // series_length = series_length+1

                    }
                }
            },
            error: function (xhr,status,error) {
                console.log(xhr)
                console.log(status)
                console.log(error)
                show_error("Error loading time series from " + res_id);
            }
        });
    }
}


function plot_data(chart, res_id, end_of_resources1, unit_off,id_qms,data){
    json = data
    var xtime = []
    var end_of_subresources =false
    //console.log(json)
    // var status = json.status;
    // if (status !== 'success') //displays error
    // {
    //     show_error(chart, "Error loading time series from " + res_id + ": " + status)
    //     $('#loading').hide();
    //     return;
    // }

    var master_values = json.master_values;
    //var master_counter = json.master_counter;
    var master_times = json.master_times;
    var meta_dic = json.meta_dic;
    var master_boxplot = json.master_boxplot
    var master_stat = json.master_stat
    var bad_meta = false
    var bad_meta_counter = 0
    var val1=[]

    var counter =0
    console.log(Object.keys(master_values).length)
    end_of_resources = Object.keys(master_values).length + end_of_resources -1
    id_qms_a_split = id_qms.split('aa')//identifier based upon url parameters
    var counter1 = 0
    console.log(master_values)

    for (val in master_values)//this loop deals with any parameters that are not specified in the url query
    {

        meta1 = val.split("aa");// an identifier based upon data in file
        if (id_qms != 'not_cuahsi')
        {
            if (id_qms_a_split[0] == '') {
                meta1[0] = ''
            }
            if (id_qms_a_split[1] == '') {
                meta1[1] = ''
            }
            if (id_qms_a_split[2] == '') {
                meta1[2] = ''
            }
        }
        if (meta_dic['quality_code'][meta1[0]] == undefined) {
            meta1[0] = ''
        }
        else {
            meta1[0] = meta_dic['quality_code'][meta1[0]]// replaces quality code with quality id
        }
        id_qms_a = id_qms_a_split[0] + 'aa' + id_qms_a_split[1] + 'aa' + id_qms_a_split[2]
        val1.push(meta1[0] + 'aa' + meta1[1] + 'aa' + meta1[2])

        if (val1[counter1] != id_qms_a) {
            bad_meta_counter += 1
        }
        counter1 = counter1+1
    }
    console.log(master_values)
    if (bad_meta_counter == Object.keys(master_values).length) {
        bad_meta = true
    }
    for (val in master_values) {
        if (bad_meta == true) {
            var arr=[]
            for (entry in val1){arr.push('')}
            val1 = arr

            id_qms_a = ''
        }
        if (id_qms_a == val1[counter] || id_qms_a == 'not_cuahsi') {
            //console.log(json)
            var m_xval = []
            var m_yval = []
            // var length_master = length_master + 1
            var meta = val.split("aa");
            var code = meta_dic['quality_code'][meta[0]]
            var quality = meta_dic['quality'][code]
            var quality_code = [meta[0]]
            var method = meta_dic['method'][meta[1]]
            var sourcedescription = meta_dic['source'][meta[2]]
            var organization = meta_dic['organization'][meta[2]]
            var m_xval = master_times[val]
            var boxplot = master_boxplot[val]
            var mean = master_stat[val][0]
            var median = master_stat[val][1]
            var max = master_stat[val][2]
            var min = master_stat[val][3]
            var m_yval = master_values[val]
            var count = m_xval.length
            var site_name = json.site_name
            var variable_name = json.variable_name
            var unit = json.units
            var units = json.units;
            var datatype = json.datatype
            var valuetype = json.valuetype
            var samplemedium = json.samplemedium
            var timesupport = json.timesupport
            var timeunit = json.timeunit
            var boxplot_count = number
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
            if (unit == null) {
                unit = 'N/A'
            }
            if (timesupport == null) {
                timesupport = "N/A"
            }
            if (timeunit == null || timeunit == ' ') {
                timeunit = "N/A"
            }
            if (sourcedescription == null) {
                sourcedescription = "N/A"
            }
            if (samplemedium == null) {
                samplemedium = "N/A"
            }
            if (units != null) {
                units = units.replace(/\s+/g, '==');//removes any spaces in the units
            }
            var unit_off_bool = false
            var y_title = null;//tracks which variable to use for the yaxis title
            var temp_date = new Date()
            // console.log('!!!!!!!!!!!!!!!!!')
            // console.log(temp_date)
            // console.log(temp_date.getMilliseconds())
            var utc_offset = temp_date.getTimezoneOffset()*1000*60
            for (i = 0; i < m_xval.length; i++)//formats values and times for the graph
            {
                var date_value = y_yval[i]
                var actual_date = (date_value*1000+utc_offset)
                var yval = null
                if (m_yval[i]!=None){
                    yval = m_yval[i]
                }
                xtime.push({x:actual_date , y: yval})
            }
            data1 = xtime
            if (unit_off == '') //unit_off stores the unit being turned off if there are more than 2 unit types
            {
                if (unit1 == null) {
                    unit1 = units
                    y_title = 0
                }
                else if (unit1 == units){
                    y_title = 0

                }
                else if (unit1 != units)//checks the first unit type agaisnt the current unit
                {
                    if (unit2 == null) {
                        y_title = 1
                        unit2 = units //this tracks the second unit type if there is one
                    }

                    else if (unit2 == units){
                        y_title = 1
                    }
                    else if (units != unit2) {
                        y_title = 3
                        console.log(units)
                        unit_off_bool = true
                    }
                }
            }
            else {
                console.log(units)
                console.log(unit_off)
                if (units != unit_off) {
                    if (units == unit1) {
                        y_title = 0
                        unit_off_bool = false
                    }
                    else if (units == unit2) {
                        y_title = 1
                        unit_off_bool = false
                    }
                    else{
                        y_title = 3
                        unit_off_bool = true
                    }
                }

                else{
                    y_title = 3
                    unit_off_bool = true
                }
            }
            if (y_title == 0) {//sets the y-axis title and graphs data on primary axis
                if (max > ymax) {
                    ymax = max
                }
                if (min < ymin) {
                    ymin = min
                }
                var newSeries =
                {
                    //type: "scatter",
                    type: "line",
                    axisYType: "primary",
                    //axisYType:"secondary",
                    xValueType: "dateTime",
                    xValueFormatString: "MMM DD, YYYY: HH:mm",
                    showInLegend: false,
                    indexLabelFontSize: 1,
                    visible: true,
                    variable: units,
                    name: 'Site: ' + site_name + ' <br/> Variable: ' + json.variable_name + '<br/> Value: ',
                    dataPoints: data1
                };
                chart.options.axisY.title = json.variable_name + ' (' + json.units + ')'
                chart.options.axisY.titleWrap = true
                // chart.options.data=[newSeries,newSeries];
                // chart.options.data.push(newSeries);
                //if (ymax == 0 && ymin == 0) {
                //    ymax = 4.5, ymin = 0
                //}
                // grid_values = gridlines(ymax,ymin)
                // chart.options.axisY.viewportMaximum = grid_values.maxview
                // chart.options.axisY.maximum = grid_values.maxview
                // chart.options.axisY.viewportMinimum = grid_values.minview
                // chart.options.axisY.minimum = grid_values.minview
                // chart.options.axisY.interval = grid_values.interval
            }
            else if (y_title == 1) {//sets the y-axis 2 title and flags that the data is graphed on the secondary axis
                // unit_off_bool = true
                if (max > y2max) {
                    y2max = max
                }
                if (min < y2min) {
                    y2min = min
                }
                var newSeries =
                {
                    type: "line",
                    //axisYType:"primary",
                    axisYType: "secondary",
                    xValueType: "dateTime",
                    xValueFormatString: "MMM DD, YYYY: HH:mm",
                    showInLegend: false,
                    indexLabelFontSize: 1,
                    variable: units,
                    visible: true,
                    name: 'Site: ' + site_name + ' <br/> Variable: ' + json.variable_name + '<br/> Value: ',
                    dataPoints: data1
                };
                chart.options.axisY2.title = json.variable_name + ' (' + json.units + ')'
                chart.options.axisY2.titleWrap = true
                // chart.options.data.push(newSeries);
                //if (y2max == 0 && y2min == 0) {
                //    y2max = 4.5, y2min = 0
                //}
                // grid_values = gridlines(y2max,y2min)
                // chart.options.axisY2.viewportMaximum = grid_values.maxview
                // chart.options.axisY2.viewportMinimum = grid_values.minview
                // chart.options.axisY2.interval = grid_values.interval
                // chart.options.axisY2.maximum = grid_values.maxview
                // chart.options.axisY2.minimum = grid_values.minview
            }
            else if (y_title == 3) {//sets the y-axis 2 title and flags that data should not be visible
                var newSeries =
                {
                    type: "line",
                    //axisYType:"primary",
                    axisYType: "primary",
                    xValueType: "dateTime",
                    showInLegend: false,
                    indexLabelFontSize: 1,
                    visible: false,
                    variable: units,
                    name: 'Site: ' + site_name + ' <br/> Variable: ' + json.variable_name + '<br/> Value: ',
                    dataPoints: data1
                };
                // chart.options.data.push(newSeries);
            }
            series_tracker.push(newSeries)

            xtime = []

            if ((unit1 != units && unit2 != units) || unit_off_bool == true)//this triggers if more than 2 different units are used
            {
                var legend = "<div style='text-align:center'><input class = 'checkbox' id =" + number + " name =" + units + " data-resid =" + res_id
                    + " type='checkbox' onClick ='series_visiblity_toggle(this.id,this.name);' unchecked>" + "</div>"
                $('#multiple_units').html("")
                $('#multiple_units').append('* Only two types of units are displayed at a time.');
                title = 1
                var chart = $("#chartContainer").CanvasJSChart()
            }
            else {
                var legend = "<div style='text-align:center' '><input class = 'checkbox' id =" + number + " name =" + units + " data-resid =" + res_id
                    + " type='checkbox' onClick ='series_visiblity_toggle(this.id,this.name);' checked>" + "</div>"
                var chart = $("#chartContainer").CanvasJSChart()
                title=0
            }

            if (quality == "N/A") {
                quality_title = "N/A"
            }
            else {
                quality_title = quality //string representing the contents of the tooltip
                if (quality.length > 20) {
                    quality = '(' + quality_code + ') ' + quality.substring(0, quality.indexOf(' ') + 1) + '...'
                }
            }
            var dataset = {
                legend: legend,
                number: number,
                organization: organization,
                name: site_name,
                variable: variable_name,
                unit: unit,
                chk_units:units,
                samplemedium: samplemedium,
                count: count,
                //download:download,
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
                boxplot: boxplot,
                boxplot_count: boxplot_count
            }
            row_tracker.push(dataset)
            // var table = $('#data_table').DataTable();//defines the primary table
            // table.row.add(dataset).draw();//adds data from the time series to the primary table
            // chart.render();//updated chart with new values
            // var temp_date = new Date()
            // console.log(temp_date)
            // console.log(temp_date.getMilliseconds())
            // console.log('!!!!!!!!!!!!!!!!!')
            number = number + 1;
            console.log(number)
        }
        counter_all =counter_all+1
        // end_of_subresources=true
        console.log(end_of_resources)
        console.log("yyyyyyyyyyyyy")
        console.log(counter_all)
        console.log(end_of_resources - counter_all)
        // if (counter_all==end_of_resources - counter_all)//checks to see if all the data is loaded before displaying
        if (0==end_of_resources - counter_all)//checks to see if all the data is loaded before displaying
        {
            display_table_chart(number)
        }


    }
    //    end of looping through timeseries

    // if (end_of_resources == true && counter ==Object.keys(master_values).length )//checks to see if all the data is loaded before displaying
    // {
    //     display_table_chart(number)
    // }
}
// Take all data and display it in the table and graph
function display_table_chart(number){
    var chart = $("#chartContainer").CanvasJSChart()
    var table = $('#data_table').DataTable();//defines the primary table
        // console.log(row_tracker)
        // var table = $('#data_table').DataTable();
        table
            .clear()
            .draw();
        // Adding data row to data for each series
        for (row in row_tracker){
            // console.log(row_tracker[row])
            table.row.add(row_tracker[row]).draw();

        }
        console.log('adding data to chart')
        // console.log(series_tracker)
        // console.log(ymax)
        // console.log(ymin)
        if (ymax == ymin){
            ymax = ymin +1
        }
         if (y2max == y2min){
            y2max = y2min +1
        }
        chart.options.data = series_tracker
        chart.options.axisY.titleFontSize = 15
        chart.options.axisY2.titleFontSize = 15
        chart.options.axisX.titleFontSize = 15

        grid_values = gridlines(y2max,y2min)
        chart.options.axisY2.viewportMaximum = grid_values.maxview
        chart.options.axisY2.viewportMinimum = grid_values.minview
        chart.options.axisY2.interval = grid_values.interval
        chart.options.axisY2.maximum = grid_values.maxview
        chart.options.axisY2.minimum = grid_values.minview

        grid_values = gridlines(ymax,ymin)
        chart.options.axisY.viewportMaximum = grid_values.maxview
        chart.options.axisY.maximum = grid_values.maxview
        chart.options.axisY.viewportMinimum = grid_values.minview
        chart.options.axisY.minimum = grid_values.minview
        chart.options.axisY.interval = grid_values.interval

        if (title == 1) {
            //chart.setTitle({ text: "CUAHSI Data Series Viewer*" });
            // chart.options.title.texft = "CUAHSI Data Series Viewer*"
            // chart.render();
        }
        else {
            //chart.setTitle({ text: "CUAHSI Data Series Viewer" });
            chart.options.title.text = "CUAHSI Data Series Viewer"
            chart.render();
        }
        $('#data_table tbody tr:eq(0) td:eq(1)').click()
        $('#data_table tbody tr:eq(0) td:eq(1)').click()
        for (i = 0; i < number; i++) {
            $('#data_table tbody tr:eq(' + i + ') td:eq(1)').click()
            $('#data_table tbody tr:eq(' + i + ') td:eq(1)').click()
        }
        finishloading();


}

function roundUp(x){
    var negative = false;
    if(x < 0) {
        negative = true;
        x *= -1;
    }
    var y = Math.pow(10, x.toString().length-1);
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
    var negative = false;
    if(x<10 && x>=0){
        x = 0

        return x
    }
    else if(x <1 && x>=-1){
        x=1
        negative = true
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
        var y = Math.pow(10, x.toString().length-1);
        x = (x/y);
        x = Math.ceil(x);
        x = x*y*-1;

        return x
    }
    var y = Math.pow(10, x.toString().length-1);
    x = (x/y);
    x = Math.floor(x);
    x = x*y;

    if(negative){
        x *= -1;
        return x;
    }
    else{
        return x;
    }
}


function series_visiblity_toggle(id, name) {
    var chart1 = $("#chartContainer").CanvasJSChart()
    var selected_box = document.getElementById(id)
    var chk_unit = document.getElementById(id).name;
    var table = $('#data_table').DataTable()

    //units = units.replace(/\s+/g, '==')
    if (name == "master_chk") {
        if (document.getElementById("master_chk").checked==true){
            //turn on everything
            for (series in chart1.options.data){
                console.log(series)
                console.log(unit1)
                console.log(unit2)



                row_up = table.rows().data()[series]
                legend = row_up.legend
                chk_unit = row_up.chk_units
                console.log(chk_unit)

                // table.fnUpdate(row_up,series,undefined,false);

                // var chk_unit = document.getElementById(series).name;
                if (chk_unit == unit1 || chk_unit == unit2){
                    row_up.legend = legend.replace('unchecked','checked')

                    chart1.options.data[series].visible = true
                    // document.getElementById(series).checked = true
                    table.row(series).data(row_up).draw()

                }

            }
        }
        else{
            console.log('turn off')
            //turn off everything
            for (series in chart1.options.data){
                row_up = table.rows().data()[series]
                legend = row_up.legend
                row_up.legend = legend.replace('checked','unchecked')
                console.log(series)
                chart1.options.data[series].visible = false
                // document.getElementById(series).checked = false
                row_up.legend = legend.replace('checked','unchecked')
                table.row(series).data(row_up).draw()

            }
        }
        chart1.render();
    }
    else {
        var res = selected_box.getAttribute("data-resid")
        var series_visibility = chart1.options.data[id].visible
        if (series_visibility == true) {
            chart1.options.data[id].visible = false
            chart1.render();
        }
        else if (series_visibility == false) {
            //first_unit =''
            if (chk_unit != unit1 && chk_unit != unit2) {
                unit1_display = unit1.replace(/==/g, ' ')
                unit2_display = unit2.replace(/==/g, ' ')
                var test1 = 'Please select a unit type to hide.<br>' +
                    '<input type="radio" id ="r1" name ="units" value=' + unit1 + ' checked>' + unit1_display + '<br>' +
                    '<input type="radio" id ="r2" name ="units" value=' + unit2 + '>' + unit2_display + '<br>' +
                    '<button class="btn btn-danger" id="change_unit" onclick ="multipletime()" >submit</button>'
                $('#' + id).attr('checked', false);
                $('#unit_selector_info').html("")
                $('#unit_selector_info').append(test1)
                unit3 = chk_unit
                var popupDiv = $('#unit_selector');
                popupDiv.modal('show');

            }
            else {
                chart1.options.data[id].visible = true
                chart1.render();
            }
        }
    }
}


/* Formatting function for row details - modify as you need */
function format(d) {
    // `d` is the original data object for the row
    name = 'container' + d.boxplot_count
    return '<div id = "container' + d.boxplot_count + '"class ="highcharts-boxplot" style = "float:right;height:300px;width:40%" ></div>' +
        '<link href="https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css" rel="stylesheet">'+
        '<script src="https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js"></script>'+
        '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:100px; margin-left:8.5%;font-size: 9pt">' +
        '<tr>' +
        '<td>Sample Medium:</td>' +
        '<td>' + d.samplemedium + '</td>' +
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
        '<tr>' +
        '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:100px; margin-left:8.5%;font-size: 9pt">'+
        '<td>Line Plot</td>'+
        '<td><label class="switch"> <input id= "'+d.number+'"type="checkbox"onClick ="scatter_line(this.id);"> <div class="slider round"></div> </label></td>' +
        '<td>' +
        '<div id="scatter'+ d.number+'">Scatter Plot</div>' +
        '' +
        '</td>' +
        '</table>'+
        '</tr>' +
        '</table>';
    //'<input type="checkbox" checked data-toggle="toggle">
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
    $("#chart").show();
    chart.render();
}


function multipletime() {
    var popupDiv = $('#unit_selector');
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
    // chart.render()
    // $("#chartContainer").html=''
    $("#chart").hide();
    ymax =0
    ymin=0
    y2max=0
    y2min=0
    series_tracker = []
    row_tracker = []
    number  = 0
    // TODO loop for chart data and turn off/on appropiate series and update checkboxes
    var table = $('#data_table').DataTable();
    table
        .clear()
        .draw();
    addingseries(unit_off);
}


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


function trim_input(string){
    string = string.replace(']','')
    string = string.replace('[','')
    string = string.replace(/'/g,'')
    string = string.replace(/"/g,'')
    string = string.replace(/ /g,'')
    //string = string.replace('[','')
    string =string.split(',')
    return string
}


function find_query_parameter(name) {
    url = location.href;
    values=[]
    url1 = url.split('?')
    if (url1[1]==undefined){values.push('')}
    else {
        url1 = url1[1].split('&')
        for (e in url1) {
            if (url1[e].indexOf(name) == 0) {
                string = url1[e]
                string = string.split('=')
                values.push(string[1])
            }
        }
    }
    return values
}


function scatter_line(id){
    var chart1 = $("#chartContainer").CanvasJSChart()
    data = chart1.options.data
    var size = Object.keys(data).length;
    var selected_box = document.getElementById(id)
    var chk_unit = document.getElementById(id).name;
    var type = chart1.options.data[id].type
    if(type =='line'){
        chart1.options.data[id].type = 'scatter'
        if (size==1){chart1.options.data[id].color='#ec3131'}//keeps the scatter plot points the same color

    }
    else{chart1.options.data[id].type='line'

    }
    chart1.render()
}


function gridlines(ymax,ymin){

    //console.log(ymax)
    //console.log(ymin)
    maxview = roundUp(Math.ceil(ymax))
    maxview = maxview + 0.1 * maxview

    minview = roundDown(Math.floor(ymin))
    minview = minview + minview * .1

    interval = Math.ceil(maxview - minview) / 11


    if (minview < 0) {
        neg_interval = Math.ceil(-1*(minview/interval))
        //pos1_interval = Math.ceil(maxview/interval)
        pos_interval = 11-neg_interval


        if (ymax> pos_interval*interval)//checks to make sure points are in view range
        {
            interval = Math.ceil(maxview/interval)*interval
        }
        if (ymin<minview){
            interval = Math.ceil(-1*minview/interval)*interval
        }

        maxview = pos_interval*interval
        minview = -1*neg_interval*interval

    }
    else {
        interval = (maxview - minview) / 11
        minview = (Math.ceil((minview / interval)) * interval)
    }
    //console.log(maxview)
    //console.log(minview)
    //console.log(interval)

    if (maxview <ymax || minview>ymin){
       interval = Math.ceil(maxview - minview) / 11
    }
    //if (5 < Math.abs(maxview)){
    ////    maxview = Math.round(maxview*100)/100
    ////    minview = Math.round(minview*100)/100
    //    interval = Math.round(interval*100)/100
    //}

    return {'maxview':maxview,'minview':minview,'interval':interval}
}
function loadMap () {
    var map = new ol.Map({
        target: 'map',
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
          })
        ],
        view: new ol.View({
          center: ol.proj.fromLonLat([37.41, 8.82]),
          zoom: 4
        })
      });
}
// Get list of HydroShare Resources
function get_list_hs_res(){
    console.log('get hs resources')


    hs_res_ids =''
    $('#map').hide();
    // hs_res_list_loaded = true
    if (hs_res_list_loaded == false) {
        setTimeout(function(){
            console.log('resize')
            $(window).trigger("resize");

        var map = new ol.Map({
            target: 'map',
            layers: [
              new ol.layer.Tile({
                source: new ol.source.OSM()
              })
            ],
            view: new ol.View({
              center: ol.proj.fromLonLat([37.41, 8.82]),
              zoom: 4
            })
          });
         }, 500);
        $('#hs_resource_table_wrapper').hide();
        var csrf_token = getCookie('csrftoken');
        var current_url = location.href;
        var index = current_url.indexOf("timeseries-viewer");
        var base_url = current_url.substring(0, index);
        data_url = base_url + "timeseries-viewer/get_hydroshare_res/";
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': csrf_token},
            dataType: 'json',
            //timeout: 5000,
            data: {'hs_res_ids': hs_res_ids},
            url: data_url,
            success: function (json) {

                error = json.error
                //console.log(json.error)
                if (error != '') {
                    show_error(error)
                }
                else {

                    var table_hs = $('#hs_resource_table').DataTable();//defines the primary table
                    // console.log(row_tracker)
                    json = json.data
                    console.log(json)
                    len = json.length
                    for (series in json) {
                        table_hs.row.add(json[series]).draw();
                        // console.log('start series')
                    }
                    $('#loading_hs').hide();
                    $('#hs_resource_table_wrapper').show();
                    $(window).resize()
                    hs_res_list_loaded = true


                }
            },
            error: function () {
                show_error("Error loading HydroShare Resources");
            }
        });
    }



}
function get_hs_res(){
    var src = 'hydroshare'
    var unit_off = ''
    var id_qms="not_cuahsi"
    var chart = $("#chartContainer").CanvasJSChart()
    var series_counter = add_hs_res.length+number
    var xml_rest_id=null
    var popupDiv = $('#modalLoadRes');
    popupDiv.modal('hide');
    $('#loading').show();
    $("#chart").hide();
    $('#stat_div').hide();
    $('#multiple_units').hide();
    series_counter = add_hs_res.length
    for (id in add_hs_res){
        length_master= 0
        current_url = location.href;
        index = current_url.indexOf("timeseries-viewer");
        base_url = current_url.substring(0, index);
        var csrf_token = getCookie('csrftoken');
        data_url = base_url + 'timeseries-viewer/chart_data/' + add_hs_res[id] + '/' + src + '/';
        $.ajax({
            type:"POST",
            headers:{'X-CSRFToken':csrf_token},
            dataType: 'json',
            //timeout: 5000,
            data:{'url_xml':xml_rest_id},
            url: data_url,
            success: function (json) {
                //console.log(json)
                var dseries =[]
                error = json.error
                console.log(json.error)
                var chart = $("#chartContainer").CanvasJSChart()
                json = json.data
                console.log(json)
                len = json.length
                var res_id_counter = 0
                if (error != ''){show_error(error)}
                else {
                    console.log(json[series])
                    var series_length = series_counter
                    for (series in json) {
                        console.log('start series')
                        res_id_counter = res_id_counter + 1
                        console.log(res_id_counter)
                        res_id_counter = res_id_counter + 1
                        if (res_id_counter == series_length){
                            end_of_data = true
                        }
                        if (json[series]['gridded'] == true) {
                            console.log('Data is gridded')
                        }
                        plot_data(chart, add_hs_res[id], series_counter + len - 1, unit_off, id_qms, json[series], len)
                    }
                }

            },
            error: function () {
                show_error("Error loading time series from " + add_hs_res[id]);
            }
        });
    }

}
// id = id of selected checkbox element
// check_box - changes status attribute for checkboxes in hydroshare resource selector
function check_box(id){
    var selected_box = document.getElementById(id)
    if($(selected_box).is(':checked')){
        $(selected_box).attr('status',"checked")
        add_hs_res.push(id)

    }
    else{
        $(selected_box).attr('status',"unchecked")
        var index = add_hs_res.indexOf(id);
        console.log(index)
        if (index > -1) {
            add_hs_res.splice(index, 1);
        }
    }
    console.log(add_hs_res)
}
// shows an error message in the chart title
function show_error(error_message) {
    $('#loading').hide();
    console.log(error_message);
    $('#error-message').text(error_message);
    console.log(series_tracker)
    if (series_tracker.length >0){
        finishloading()
    }
}
function get_screenshot() {
    var myDiv = document.getElementById('app-content-wrapper');
    myDiv.scrollTop = 0;
    $("tfoot").hide()
    console.log(screen.width)
    html2canvas(document.body, {
        onrendered: function (canvas) {
            console.log(canvas)
            canvas.setAttribute("id", "canvas_print")

            var print = document.getElementById('print_div');
            print.innerHTML =""
            var link = document.getElementById('download');

            myDiv.scrollTop = 0;
            print.appendChild(canvas);
            var canvas = document.getElementById("canvas_print");
            console.log(link)
            link.href = canvas.toDataURL("image/png");
            // link.href    = canvas.toDataURL();
            link.download = 'data_series_viewer.png'
            console.log(link)
            $("#download")[0].click()
            $("tfoot").show()
        },
        width: $(document).width(),
        height:$('#app-content-wrapper')[0].scrollHeight
        // height: 1500
    });
    // canvas = html2canvas(document.getElementById('chartContainer') , {
    //     onrendered: function (canvas) {
    //         console.log(canvas)
    //         canvas.setAttribute("id", "canvas_print")
    //         var myDiv = document.getElementById('app-content-wrapper');
    //         var print = document.getElementById('print_div');
    //         var link = document.getElementById('download');
    //
    //         myDiv.scrollTop = 0;
    //         print.appendChild(canvas);
    //         var canvas = document.getElementById("canvas_print");
    //         console.log(link)
    //         link.href = canvas.toDataURL("image/png");
    //         // link.href    = canvas.toDataURL();
    //         link.download = 'canvas_test.png'
    //         console.log(link)
    //         $("#download")[0].click()
    //     },
    //     width: 1300,
    //     height: 1300
    // });
    // console.log(canvas)
}

