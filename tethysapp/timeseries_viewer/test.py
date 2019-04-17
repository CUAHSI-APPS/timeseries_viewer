def parse_1_0_and_1_1(root):
    root_tag = root.tag.lower()
    boxplot = []
    master_values=collections.OrderedDict()
    master_times = collections.OrderedDict()
    master_boxplot = collections.OrderedDict()
    master_stat = collections.OrderedDict()
    master_data_values = collections.OrderedDict()
    meth_qual = [] # List of all the quality, method, and source combinations
    for_canvas = []
    meta_dic ={'method':{},'quality':{},'source':{},'organization':{},'quality_code':{}}
    m_des = []
    m_code = []
    m_org =[]
    x_value = []
    y_value = []
    master_counter =True
    nodata = "-9999"  # default NoData value. The actual NoData value is read from the XML noDataValue tag
    timeunit=None
    sourcedescription = None
    timesupport =None
    # metadata items
    units, site_name, variable_name,quality,method, organization = None, None, None, None, None, None
    unit_is_set = False
    datatype = None
    valuetype = None
    samplemedium = None
    # we only display the first 50000 values
    threshold = 50000000
    try:
        if 'timeseriesresponse' in root_tag or 'timeseries' in root_tag or "envelope" in root_tag or 'timeSeriesResponse' in root_tag:
            print(root_tag)
            # lists to store the time-series data

            # iterate through xml document and read all values
            for element in root.iter():
                bracket_lock = -1
                if '}' in element.tag:
                    # print element.tag
                    bracket_lock = element.tag.index('}')  # The namespace in the tag is enclosed in {}.
                    tag = element.tag[bracket_lock+1:]     # Takes only actual tag, no namespace

                    if 'value'!= tag:
                        # in the xml there is a unit for the value, then for time. just take the first
                        if 'unitName' == tag or 'units' ==tag or 'UnitName'==tag or 'unitCode'==tag:
                            if not unit_is_set:
                                units = element.text
                                unit_is_set = True
                        if 'noDataValue' == tag:
                            nodata = element.text
                        if 'siteName' == tag:
                            site_name = element.text
                        if 'variableName' == tag:
                            variable_name = element.text
                        if 'organization'==tag or 'Organization'==tag or'siteCode'==tag:
                            try:
                                organization = element.attrib['agencyCode']
                            except:
                                organization = element.text
                        if 'definition' == tag or 'qualifierDescription'==tag:
                            quality = element.text
                        if 'methodDescription' == tag or 'MethodDescription'==tag:
                            # print element.attrib['methodID']
                            method = element.text
                        if 'dataType' == tag :
                            datatype = element.text
                        if 'valueType' == tag:
                            valuetype = element.text
                        if "sampleMedium" == tag:
                            samplemedium = element.text
                        if "timeSupport"== tag or"timeInterval" ==tag:
                            timesupport =element.text
                        if"unitName"== tag or "UnitName"==tag:
                            timeunit =element.text
                        if"sourceDescription"== tag or "SourceDescription"==tag:
                            sourcedescription =element.text

                        if "method" ==tag:
                            for subele in element:
                                bracket_lock = subele.tag.index('}')  # The namespace in the tag is enclosed in {}.
                                tag1 = element.tag[bracket_lock+1:]
                                # Takes only actual tag, no namespace
                                if 'methodCode' in subele.tag:
                                    m_code = subele.text
                                if 'methodDescription' in subele.tag:
                                    m_des = subele.text
                            meta_dic['method'].update({m_code:m_des})
                        if "source" ==tag:
                            for subele in element:
                                bracket_lock = subele.tag.index('}')  # The namespace in the tag is enclosed in {}.
                                tag1 = element.tag[bracket_lock+1:]
                                # Takes only actual tag, no namespace
                                if 'sourceCode' in subele.tag:
                                    m_code = subele.text
                                if 'sourceDescription' in subele.tag:
                                    m_des = subele.text
                                if 'organization' in subele.tag:
                                    m_org = subele.text
                            meta_dic['source'].update({m_code:m_des})
                            meta_dic['organization'].update({m_code:m_org})
                        if "qualityControlLevel" ==tag:
                            for subele in element:
                                bracket_lock = subele.tag.index('}')  # The namespace in the tag is enclosed in {}.
                                tag1 = element.tag[bracket_lock+1:]
                                # Takes only actual tag, no namespace
                                if 'qualityControlLevelCode' in subele.tag:
                                    m_code = subele.text
                                if 'definition' in subele.tag:
                                    m_des = subele.text
                            meta_dic['quality'].update({m_code:m_des})

                    elif 'value' == tag:
                        # print element.attrib
                        try:
                            n = element.attrib['dateTimeUTC']
                        except:
                            n =element.attrib['dateTime']
                        try:
                            quality= element.attrib['qualityControlLevelCode']
                        except:
                            quality1 =''
                        try:
                            method = element.attrib['methodCode']
                        except:
                            method=''
                        try:
                            source = element.attrib['sourceCode']
                        except:
                            source=''
                        dic = quality +'aa'+method+'aa'+source
                        if dic not in meth_qual:
                            meth_qual.append(dic)
                            master_values.update({dic:[]})
                            master_times.update({dic:[]})
                            master_boxplot.update({dic:[]})
                            master_stat.update({dic:[]})
                            master_data_values.update({dic:[]})

                        v = element.text
                        if v == nodata:
                            value = None
                            x_value.append(n)
                            y_value.append(value)
                            v =None

                        else:
                            v = float(element.text)
                            x_value.append(n)
                            y_value.append(v)
                            master_data_values[dic].append(v) #records only none null values for running statistics
                        master_values[dic].append(v)
                        master_times[dic].append(n)

            for item in master_data_values:
                if len(master_data_values[item]) ==0:
                    mean = None
                    median =None
                    quar1 = None
                    quar3 = None
                    min1 = None
                    max1=None
                else:
                    mean = numpy.mean(master_data_values[item])
                    mean = float(format(mean, '.2f'))
                    median = float(format(numpy.median(master_data_values[item]), '.2f'))
                    quar1 = float(format(numpy.percentile(master_data_values[item],25), '.2f'))
                    quar3 = float(format(numpy.percentile(master_data_values[item],75), '.2f'))
                    min1 = float(format(min(master_data_values[item]), '.2f'))
                    max1 = float(format(max(master_data_values[item]), '.2f'))
                master_stat[item].append(mean)
                master_stat[item].append(median)
                master_stat[item].append(max1)
                master_stat[item].append(min1)
                master_boxplot[item].append(1)
                master_boxplot[item].append(min1)#adding data for the boxplot
                master_boxplot[item].append(quar1)
                master_boxplot[item].append(median)
                master_boxplot[item].append(quar3)
                master_boxplot[item].append(max1)

            return {
                'site_name': site_name,
                'variable_name': variable_name,
                'units': units,
                'meta_dic':meta_dic,
                'for_canvas':for_canvas,
                'organization': organization,
                'quality': quality,
                'method': method,
                'status': 'success',
                'datatype' :datatype,
                'valuetype' :valuetype,
                'samplemedium':samplemedium,
                'timeunit':timeunit,
                'sourcedescription' :sourcedescription,
                'timesupport' : timesupport,
                'master_counter':master_counter,
                'boxplot':boxplot,
                'master_values':master_values,
                'master_times':master_times,
                'master_boxplot':master_boxplot,
                'master_stat':master_stat
            }
        else:
            parse_error = "Parsing error: The WaterML document doesn't appear to be a WaterML 1.0/1.1 time series"
            error_report("Parsing error: The WaterML document doesn't appear to be a WaterML 1.0/1.1 time series")
            print(parse_error)
            return {
                'status': parse_error
            }
    except Exception, e:
        data_error = "Parsing error: The Data in the Url, or in the request, was not correctly formatted for water ml 1."
        error_report("Parsing error: The Data in the Url, or in the request, was not correctly formatted.")
        print(data_error)
        print(e)
        return {
            'status': data_error
        }