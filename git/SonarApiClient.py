import json
# from lib2to3.pgen2 import token
import os
#from tkinter import N
import requests
from datetime import datetime
import pandas as pd


class SonarApiClient:

    def __init__(self, token):
        self.token = token
        self.BASE_URL = 'https://sonarcloud.io/'

    def _make_request(self, endpoint):
        r = requests.get(self.BASE_URL + endpoint, auth=(self.token, ''))
        return r.json()

    def get_all_ids(self, endpoint):
        data = self._make_request(endpoint)
        ids = []
        for component in data['components']:
            dict = {
                'id': component['name'],
                'key': component['key']
            }
            ids.append(dict)
        return ids

    def get_all_available_metrics(self, endpoint):
        data = self._make_request(endpoint)
        metrics = []
        for metric in data['metrics']:
            metrics.append(metric['key'])
        return metrics

    def get_measures_by_component_id(self, endpoint):
        data = self._make_request(endpoint)
        print(data)
        return data['component']['measures']

    def get_files_by_component_id(self, project_id):
        list_to_export = []
        endpoint = 'api/components/tree?component='+project_id+'&qualifiers=FIL&ps=500'
        print(endpoint)
        data = self._make_request(endpoint)
        for s in range(len(data["components"])):
            list_to_export.append(data["components"][s]['path'])
        return list_to_export

    def get_measures_by_file(self, endpoint):
        data = self._make_request(endpoint)
        return data

    

def get_dict_and_string(metrics_api,metrics_to_use):
    final_metrics = []
    comma_separated_metrics = ''
    for metric in metrics:
        if metric in include_these_metrics:
            comma_separated_metrics += metric + ','
            final_metrics.append(metric)
    comma_separated_metrics = comma_separated_metrics[:-1]
    empty_list = [[] for _ in range(len(final_metrics))]
    value_dict = dict(zip(final_metrics,empty_list))
    return value_dict,comma_separated_metrics

def get_dataframe(client,ids,project_to_scan,dictonary):
    uri = 'api/measures/component'
    value_dict = dictonary
    # Loop through projects
    for item in ids:
        metric_key_query_param = 'metricKeys=' + comma_separated_metrics
        qualifier_query_param = 'qualifiers=FIL'
        project_id = item['id']
        project_key = item['key']
        if project_id in project_to_scan:
            files = client.get_files_by_component_id('Arvid-new_'+project_id)
            counter = 0
            for file in files:
                print('hej')
                #Fix Query to collect correct file measurement data
                component_id_query_param = 'component=' + 'Arvid-new_' + project_id + ":" + file
                #Collecting data
                measures = client.get_measures_by_file(uri + '?' + component_id_query_param + '&' + metric_key_query_param)
                fileName = measures['component']['name']
                fileMetrics = measures['component']['measures']
                path = measures['component']['path']
                for i in range(len(fileMetrics)):
                    value_dict[fileMetrics[i]['metric']].append(fileMetrics[i]['value'])

                counter += 1
            df = pd.DataFrame(value_dict)
    
    return df,counter


client = SonarApiClient('970a36cc37dfb60d1ab07301ed8b7ec9457f4ea7')
ids = client.get_all_ids('api/components/search?organization=arvid-new')

metrics = client.get_all_available_metrics('api/metrics/search')

include_these_metrics = ['duplicated_lines', 'cognitive_complexity', 'ncloc', 'functions', 'complexity', 
                         'duplicated_files', 'code_smells', 'comment_lines', 'coverage', 'duplicated_blocks']


value_dict,comma_separated_metrics = get_dict_and_string(metrics,include_these_metrics)

#get metrics from client
# metric_key_query_param = 'metricKeys=' + comma_separated_metrics
# qualifier_query_param = 'qualifiers=FIL'
# Collect metrics per project & File
projects_to_scan = ['glazedlists-tutorial']


df,counter = get_dataframe(client,ids,projects_to_scan,value_dict)
print(df.head())
print(counter)


# uri = 'api/measures/component'
# # Loop through projects
# for item in ids:
#     project_id = item['id']
#     project_key = item['key']
#     if project_id in projects_to_scan:
#         files = client.get_files_by_component_id('Arvid-new_'+project_id)
#         counter = 0
#         for file in files:
#             print('hej')
#             #Fix Query to collect correct file measurement data
#             component_id_query_param = 'component=' + 'Arvid-new_' + project_id + ":" + file
#              #Collecting data
#             measures = client.get_measures_by_file(uri + '?' + component_id_query_param + '&' + metric_key_query_param)
#             print(measures)
#             fileName = measures['component']['name']
#             fileMetrics = measures['component']['measures']
#             path = measures['component']['path']
#             for i in range(len(fileMetrics)):
#                 value_dict[fileMetrics[i]['metric']].append(fileMetrics[i]['value'])

#             counter += 1
#         df = pd.DataFrame(value_dict)
# print(df.head())