import os
import shutil
import logging
import sqlite3
from lxml import etree
import csv
from dateutil import parser
import tempfile



import pandas as pd
import numpy as np
from lxml import etree as ET
from suds.client import Client
import requests
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt

def validate_odm2_db_file(sqlite_file_path):
    """
    Validates if the sqlite file *sqlite_file_path* is a valid ODM2 sqlite file
    :param sqlite_file_path: path of the sqlite file to be validated
    :return: If validation fails then an error message string is returned otherwise None is
    returned
    """
    err_message = "Uploaded file is not a valid ODM2 SQLite file."
    log = logging.getLogger()
    try:
        con = sqlite3.connect(sqlite_file_path)
        with con:

            # TODO: check that each of the core tables has the necessary columns

            # check that the uploaded file has all the tables from ODM2Core and the CV tables
            cur = con.cursor()
            odm2_core_table_names = ['People', 'Affiliations', 'SamplingFeatures', 'ActionBy',
                                     'Organizations', 'Methods', 'FeatureActions', 'Actions',
                                     'RelatedActions', 'Results', 'Variables', 'Units', 'Datasets',
                                     'DatasetsResults', 'ProcessingLevels', 'TaxonomicClassifiers',
                                     'CV_VariableType', 'CV_VariableName', 'CV_Speciation',
                                     'CV_SiteType', 'CV_ElevationDatum', 'CV_MethodType',
                                     'CV_UnitsType', 'CV_Status', 'CV_Medium',
                                     'CV_AggregationStatistic']
            # check the tables exist
            for table_name in odm2_core_table_names:
                cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type=? AND name=?",
                            ("table", table_name))
                result = cur.fetchone()
                if result[0] <= 0:
                    err_message += " Table '{}' is missing.".format(table_name)
                    log.info(err_message)
                    return err_message

            # check that the tables have at least one record
            for table_name in odm2_core_table_names:
                if table_name == 'RelatedActions' or table_name == 'TaxonomicClassifiers':
                    continue
                cur.execute("SELECT COUNT(*) FROM " + table_name)
                result = cur.fetchone()
                if result[0] <= 0:
                    err_message += " Table '{}' has no records.".format(table_name)
                    log.info(err_message)
                    return err_message
        return None
    except sqlite3.Error, e:
        sqlite_err_msg = str(e.args[0])
        log.error(sqlite_err_msg)
        return sqlite_err_msg
    except Exception, e:
        log.error(e.message)
        return e.message

def extract_metadata(sqlite_file_name):
    """
    Extracts metadata from the sqlite file *sqlite_file_name" and adds metadata at the resource
    and/or file level
    :param resource: an instance of BaseResource
    :param sqlite_file_name: path of the sqlite file
    :param logical_file: an instance of TimeSeriesLogicalFile if metadata needs to be part of the
    logical file
    :return:
    """
    err_message = "Not a valid ODM2 SQLite file"
    log = logging.getLogger()
    try:
        con = sqlite3.connect(sqlite_file_name)
        with con:
            # get the records in python dictionary format
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            # populate the lookup CV tables that are needed later for metadata editing

            # read data from necessary tables and create metadata elements
            # extract core metadata

            # extract abstract and title
            cur.execute("SELECT DataSetTitle, DataSetAbstract FROM DataSets")
            dataset = cur.fetchone()
            # update title element


            # create abstract/description element

            # extract keywords/subjects
            # these are the comma separated values in the VariableNameCV column of the Variables
            # table
            cur.execute("SELECT VariableID, VariableNameCV FROM Variables")
            variables = cur.fetchall()
            keyword_list = []
            for variable in variables:
                keywords = variable["VariableNameCV"].split(",")
                keyword_list = keyword_list + keywords



            # extract extended metadata
            cur.execute("SELECT * FROM Sites")
            sites = cur.fetchall()
            is_create_multiple_site_elements = len(sites) > 1

            cur.execute("SELECT * FROM Variables")
            variables = cur.fetchall()
            is_create_multiple_variable_elements = len(variables) > 1

            cur.execute("SELECT * FROM Methods")
            methods = cur.fetchall()
            is_create_multiple_method_elements = len(methods) > 1

            cur.execute("SELECT * FROM ProcessingLevels")
            processing_levels = cur.fetchall()
            is_create_multiple_processinglevel_elements = len(processing_levels) > 1

            cur.execute("SELECT * FROM TimeSeriesResults")
            timeseries_results = cur.fetchall()
            is_create_multiple_timeseriesresult_elements = len(timeseries_results) > 1

            cur.execute("SELECT * FROM Results")
            results = cur.fetchall()
            for result in results:
                # extract site element data
                # Start with Results table to -> FeatureActions table -> SamplingFeatures table
                # check if we need to create multiple site elements
                cur.execute("SELECT * FROM FeatureActions WHERE FeatureActionID=?",
                            (result["FeatureActionID"],))
                feature_action = cur.fetchone()
                cur.execute("SELECT * FROM SamplingFeatures WHERE SamplingFeatureID=?",
                            (feature_action["SamplingFeatureID"],))
                sampling_feature = cur.fetchone()

                cur.execute("SELECT * FROM Sites WHERE SamplingFeatureID=?",
                            (feature_action["SamplingFeatureID"],))
                site = cur.fetchone()

                data_dict = {}
                data_dict['series_ids'] = [result["ResultUUID"]]
                data_dict['site_code'] = sampling_feature["SamplingFeatureCode"]
                data_dict['site_name'] = sampling_feature["SamplingFeatureName"]
                if sampling_feature["Elevation_m"]:
                    data_dict["elevation_m"] = sampling_feature["Elevation_m"]

                if sampling_feature["ElevationDatumCV"]:
                    data_dict["elevation_datum"] = sampling_feature["ElevationDatumCV"]

                if site["SiteTypeCV"]:
                    data_dict["site_type"] = site["SiteTypeCV"]

                data_dict["latitude"] = site["Latitude"]
                data_dict["longitude"] = site["Longitude"]

                # create site element


                # extract variable element data
                # Start with Results table to -> Variables table

                cur.execute("SELECT * FROM Variables WHERE VariableID=?",
                                (result["VariableID"],))
                variable = cur.fetchone()

                data_dict = {}
                data_dict['series_ids'] = [result["ResultUUID"]]
                data_dict['variable_code'] = variable["VariableCode"]
                data_dict["variable_name"] = variable["VariableNameCV"]
                data_dict['variable_type'] = variable["VariableTypeCV"]
                data_dict["no_data_value"] = variable["NoDataValue"]
                if variable["VariableDefinition"]:
                    data_dict["variable_definition"] = variable["VariableDefinition"]

                if variable["SpeciationCV"]:
                    data_dict["speciation"] = variable["SpeciationCV"]

                # create variable element


                # extract method element data
                # Start with Results table -> FeatureActions table to -> Actions table to ->
                # Method table
                cur.execute("SELECT MethodID from Actions WHERE ActionID=?",
                            (feature_action["ActionID"],))
                action = cur.fetchone()
                cur.execute("SELECT * FROM Methods WHERE MethodID=?", (action["MethodID"],))
                method = cur.fetchone()


                data_dict = {}
                data_dict['series_ids'] = [result["ResultUUID"]]
                data_dict['method_code'] = method["MethodCode"]
                data_dict["method_name"] = method["MethodName"]
                data_dict['method_type'] = method["MethodTypeCV"]

                if method["MethodDescription"]:
                    data_dict["method_description"] = method["MethodDescription"]

                if method["MethodLink"]:
                    data_dict["method_link"] = method["MethodLink"]


                # extract processinglevel element data
                # Start with Results table to -> ProcessingLevels table

                cur.execute("SELECT * FROM ProcessingLevels WHERE ProcessingLevelID=?",
                            (result["ProcessingLevelID"],))
                pro_level = cur.fetchone()

                data_dict = {}
                data_dict['series_ids'] = [result["ResultUUID"]]
                data_dict['processing_level_code'] = pro_level["ProcessingLevelCode"]
                if pro_level["Definition"]:
                    data_dict["definition"] = pro_level["Definition"]

                if pro_level["Explanation"]:
                    data_dict["explanation"] = pro_level["Explanation"]

                # create processinglevel element


                # extract data for TimeSeriesResult element
                # Start with Results table

                data_dict = {}
                data_dict['series_ids'] = [result["ResultUUID"]]
                data_dict["status"] = result["StatusCV"]
                data_dict["sample_medium"] = result["SampledMediumCV"]
                data_dict["value_count"] = result["ValueCount"]

                cur.execute("SELECT * FROM Units WHERE UnitsID=?", (result["UnitsID"],))
                unit = cur.fetchone()
                data_dict['units_type'] = unit["UnitsTypeCV"]
                data_dict['units_name'] = unit["UnitsName"]
                data_dict['units_abbreviation'] = unit["UnitsAbbreviation"]

                cur.execute("SELECT AggregationStatisticCV FROM TimeSeriesResults WHERE "
                            "ResultID=?", (result["ResultID"],))
                ts_result = cur.fetchone()
                data_dict["aggregation_statistics"] = ts_result["AggregationStatisticCV"]


            return None

    except sqlite3.Error as ex:
        sqlite_err_msg = str(ex.args[0])
        log.error(sqlite_err_msg)
        return sqlite_err_msg
    except Exception as ex:
        log.error(ex.message)
        return err_message
file_path = '/home/matthew/tethysdev/timeseries_viewer/tethysapp/timeseries_viewer/workspaces/app_workspace/miguel_odm2.sqlite'
# print validate_odm2_db_file(file_path)
# print extract_metadata(file_path)

def parse_waterml(waterml_string):
    root = ET.fromstring(waterml_string)
    x = None
    y = None
    x_dates = None
    print 'parsing waterml data'
    time_series = root.findall(
        './/{http://www.cuahsi.org/waterML/1.1/}timeSeries')
    nodata = root.findtext(
        './/{http://www.cuahsi.org/waterML/1.1/}noDataValue')
    variable = root.findtext(
        './/{http://www.cuahsi.org/waterML/1.1/}variableName')
    for series in time_series:
        x = []
        y = []
        x_dates = []
        values = series.findall(
            './/{http://www.cuahsi.org/waterML/1.1/}value')
        statistic = series.findtext(
            './/{http://www.cuahsi.org/waterML/1.1/}option')
        for element in values:
            date = element.attrib['dateTime']
            date = date.replace('T', ' ')
            x.append(date)
            x_dates.append(dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date())
            v = element.text
            if nodata in v or v in nodata:
                value = None
                y.append(value)
                y1 = value
            else:
                v = float(v)
                y.append(float(v))
                y1 = v
        if variable is None:
            variable = ''
        if y == []:
            variable = 'no data'
    values = {
        'dates': x,
        'values': y,
        'x_dates': x_dates
    }
    return values


def get_sites(url, site_code):
    try:
        client = Client(url)

    except:
        print 'could not connect'
    print client
    response = client.service.GetSitesByBoxObject(west=-120,south=40,east=-110,north=50,IncludeSeries=True,authToken='')
    return response

def get_variables(url, variable_code):
    try:
        client = Client(url)
        response = client.service.GetVariables(variable_code)
    except:
        print 'could not connect'
    return response

def get_values(url, site_code, variable_code, start_date, end_date, auth_token):
    try:
        client = Client(url)

    except:
        print 'could not connect'
    response = client.service.GetValues(site_code,
                                        variable_code,
                                        start_date,
                                        end_date,
                                        auth_token)
    return response

# url = 'http://dev-hydroportal.cuahsi.org/CocoRaHs/cuahsi_1_1.asmx?WSDL'
# site_code = 'COCORAHS:US1NJCD0008'
# variable_code = 'COCORAHS:PRCP'
# start_date = '2010-10-01'
# end_date = '2018-01-30'
# Get values from hydroserver
url = 'http://hydroportal.cuahsi.org/nwisdv/cuahsi_1_1.asmx?WSDL'
# Provo River at Provo Utah
site_code = 'NWISDV:01553240'
variable_code = 'NWISDV:00060/DataType=MEAN'
start_date = '2018-04-01'
end_date = '2018-04-05'
sites = get_sites(url, site_code)

print sites
# print get_variables(url, [variable_code])
# values = get_values(url, site_code, variable_code, start_date, end_date, auth_token=None)
# print values
