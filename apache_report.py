#!/usr/bin/env python3

'''CPSC 254 - Fall 2015 - Apache Log Analyzer'''

from collections import namedtuple
from apache_info import apache_log_infos
from apache_print import (print_header,
                          print_total_sent,
                          print_top_cumulative_size_requests,
                          print_status_404_requests,
                          print_weekly_unique_hosts)

def get_bytes(data_dicts):
    bytes = 0
    for data_dict in data_dicts:
        bytes += int(data_dict['size'])
    return bytes

def get_cumulative_size_request(apache_data):
    return sorted(apache_data, key=lambda k: k['size'], reverse=True)[:100]

def request_frequency(apache_data):
    data = {}

    for line in apache_data:
        if 'request' in line:
            if line['request'] in data:
                data[line['request']] += 1
            else:
                data[line['request']] = 1

    return data.items()

def get_status_404_request(apahe_data):
    data = request_frequency(apache_data)

    for line in data:
        if line['status'] != 404:
            data.remove(line)

    return sorted(data, key=lambda k: k['request'], reverse=True)

def unique_hosts(apache_data):
    request = []

    for line in apache_data:
        if 'host' in line:
            request.append(line['host'])

    return list(set(request))

def get_weekly_uniq_hosts(apache_data):
    request = []

    for line in apache_data:
        line['week'] = datetime.date(line['year'], line['month'], line['year']).isocalendar()[1]

        request.append(line)
    
    request = sorted(request, key=lambda k: k['week'])
  
    #for line in request:
    uh = []
    lw = []
    for value, index in enumerate(request):
        if(index != 0 and value['week'] != request[index-1]['week']):
            uh.append(unique_hosts(lw))
            lw = value
        else:
            lw.append(value)            
    uh.append(unique_hosts(lw))
    return uh


def aggregate_data(top_dir, file_pattern):
    '''Given the diretory path for top directory `top_dir` and the filename
    pattern to search, return a tuple of all required information to write to
    report. The report includes the following info:

        * how many bytes were sent
        * the top 100 largest cumulative size requests
        * the number of all unique host IP addresses per week
        * all 404-status requests sorted by its frequency
    '''
    Data = namedtuple('Data', 'total_sent, cumulative_size_requests, \
                      weekly_uniq_hosts, status_404_requests')

    total_sent              = 0
    cumulative_size_requests= {}
    status_404_requests     = {}
    weekly_uniq_hosts       = {}

    # +++your code here+++
    apache_data             = apache_log_infos(top_dir, file_pattern)
    total_sent              = get_bytes(apache_data)
    cumulative_size_request = get_cumulative_size_request(apache_data)
    status_404_request      = get_status_404_request(apache_data) 
    weekly_uniq_hosts       = get_weekly_uniq_hosts(apache_data)    
 
    return Data(total_sent, cumulative_size_requests,
                weekly_uniq_hosts, status_404_requests)


def print_report(file_report, data):
    '''Given the path of the report file `file_report` and the aggregated data
    form aggregate_data fucntion `data`, print the apache log report by using
    all print functions in the apache_print module. See docstring of
    apache_print module and its functions for more details. We want to print
    in the following order:

    1. Header
    2. Total byte sent
    3. Top 100 largest cumulative size requests
    4. The number of all unique host IP addresses per week
    5. All status-404 requests sorted by its frequency
    '''
    print_header(file_report)

    print_total_sent(file_report, get_bytes(data))

    print_top_cumulative_size_requests(file_report, get_cumulative_size_request(data))      

    print_status_404_requests(file_report, get_status_404_request(data))

     

def main():
    '''Run create_report function to create report'''
    data = aggregate_data('apache-log', 'access_log.*')
    print_report('apache_report.txt', data)


if __name__ == '__main__':
    main()
