'''CPSC 254 - Fall 2015 - Apache Log Analyzer Project

This module is to create generator for apache log info.
'''

import os
import bz2
import re
import gzip
import datetime


#testing

def gen_matched_files(top_dir, file_pattern):
    '''Given the top directory path `top_dir` and a file pattern
    `file_pattern`, create a generator of all the file paths that are
    matched with the given file pattern.

    Hint:
        os.walk function reference:
            https://docs.python.org/3.4/library/os.html#os.walk
    '''
    # +++your code here+++
    for path, _, file_list in os.walk(top_dir):
        for filename in file_list:
            if re.match(file_pattern, filename):    
                # file_pattern could be r'acess_log.*'
                print(os.path.join(path, filename))
                yield os.path.join(path, filename)


def gen_file_objects(file_paths):
    '''Given the file path generator `file_paths`, create a generator of all
    file objects. There are 2 types of files: bzip2-compressed files, which
    has bz2 file extension, and other text files. Use appropriate functions
    to open them.
    '''
    # +++your code here+++
    for file_path in file_paths:
        if file_path.endswith('.gz'):
            with gzip.open(file_path, mode='rt') as gz_file:
                yield gz_file
        if file_path.endswith('.bz2'):
            with bz2.open(file_path, mode='rt') as bz2_file:
                yield bz2_file
        else:
            with open(file_path) as text_file:
                yield text_file

def gen_lines(file_objects):
    '''Given the file object generator `file_objects`, create a generator of
    all lines in that file.
    '''
    # +++ your code here+++
    for file_object in file_objects:
        for line in file_object:
            yield line


def gen_log_infos(lines):
    '''Given the line generator `lines`, create a generator of a dictionary
    of info in each line of apache log. Here's what ONE line of apache log
    looks like:

    cys-cap-9.wyoming.com - - [31/Aug/1995:23:55:51 -0400] "GET
        /shuttle/missions/sts-71/movies/sts-71-launch-3.mpg HTTP/1.0" 200 49152
    ...

    The above log line prodvides the following information:
    {'host'    : 'cys-cap-9.wyoming.com',
     'referrer': '-',
     'user'    : '-',
     'day'     : 31,
     'month'   : 'Aug',
     'year'    : 1995,
     'time'    : '23:55:51',
     'timezone': '-0400',
     'method'  : 'GET',
     'request' : '/shuttle/missions/sts-71/movies/sts-71-launch-3.mpg',
     'proto'   : 'HTTP/1.0',
     'status'  : 200,
     'size'    : 49152}

    Your return info should have at least the following keys, which are host, week,
    year, requests, status, size, so that we can aggregate data later in 
    aggregate_data function in apache_report file.

    Note:
        If no byte is sent, size shows '-' instead of 0. You need to check that 
            and convert it to 0.
    '''
    # +++your code here+++
    month_dict = {'Jan': 1, 'Feb': 2,  'Mar': 3,  'Apr': 4,
              'May': 5, 'Jun': 6,  'Jul': 7,  'Aug': 8,
              'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    for line in lines:
        try:
            words = line.split()
            if len(words) != 10 or words[0] == '---':
                continue
            host = words[0]
            referrer = words[1]
            user = words[2]
            dates = words[3].replace("[","")
            dates = dates.split('/')
            day = dates[0]
            month = dates[1]
            year_and_time = dates[2].split(':', 1)
            year = year_and_time[0]
            time = year_and_time[1]
            timezone = words[4].replace("[","")
            method = words[5].replace('"', '')
            request = words[6]
            proto = words[7].replace('"', '')
            status = words[8]
            size = words[9]
            yield {'host' : host,
                   'referrer' : referrer,
                   'user' : user,
                   'dates' : dates,
                   'day' : day,
                   'month' : month_dict[month],
                   'year' : year,
                   'time' : time,
                   'timezone' : timezone,
                   'method' : method,
                   'request' : request,
                   'proto' : proto,
                   'status' : status,
                   'size' : 0 if size == '-' else int(size)
                }
        except IndexError:
            hdgfd = 3

def apache_log_infos(top_dir, file_pattern):
    '''Given the top directory `top_dir` and file pattern `file_pattern`,
    return the generator object of the info dictionary. You should combine
    from all above generators (gen_matched_files, gen_file_objects, gen_lines,
    gen_log_infos) in this function so that we will use this generator object
    to create report.
    '''
    # +++your code here+++
    matched_files = gen_matched_files(top_dir, file_pattern)
    file_objects = gen_file_objects(matched_files)
    lines = gen_lines(file_objects)
    log_infos = gen_log_infos(lines)
    return log_infos
