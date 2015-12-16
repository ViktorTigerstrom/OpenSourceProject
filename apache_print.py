'''CPSC 254 - Fall 2015 - Apache Log Analyzer

This module is to handle different print functions.
'''
import datetime


def to_human_readable_size(size):
    '''Given a integer `size` in bytes, return the tuple of human-readable-size
    floating number and its corresponding unit. See the humansize.py in the
    textbook to how to convert to human-readable size.
    '''
    # +++your code here+++
    suffixes = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']}
    if size < 0:
        raise ValueError('number must be non-negative')
    
    multiple = 1000
    for suffix in suffixes[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')


def print_header(file_report):
    '''Given the path of the report file, (over)write to the file the header
    of the report. The header should be similar to below except the date and
    time. It should be close to the date and time you run the script.

    ************************************
    *        APACHE LOG REPORT         *
    * Generated on 2015-04-19 09:04 PM *
    ************************************

    Note:
        - See datetime module reference:
            https://docs.python.org/3.4/library/datetime.html
        - To get the current date and time, see datetime.now function
        - To return formatted date and time, see datetime.strftime function
    '''
    # +++your code here+++


def print_total_sent(file_report, bytes_sent):
    '''Given file path of the report `file_report` and the total bytes
    transferred to remote hosts `bytes_sent`, write to the file after the
    header the total of bytes that is cumulated from all the apache log files.
    See the print-format below:

    Total transferred: xx.xx GB
    '''
    # +++your code here+++


def print_top_cumulative_size_requests(file_report, cumulative_size_requests):
    '''Given the path of a report file `file_report` and cumulative size of
    each request, write to the given file the top 100 largest-size requests
    and their sizes in decending order of the size from largest to less. See
    the print-format below:

    Top 100 Largest Total-Sent Requests
    /shuttle/missions/sts-71/movies/sts-71-launch.mpg 3.19 GB
    /shuttle/missions/sts-71/movies/sts-71-mir-dock.mpg 1.41 GB
    ...
    '''
    # +++your code here+++


def print_weekly_unique_hosts(file_report, weekly_uniq_hosts):
    '''Given the path of a report file `file_report` and all the unique hosts
    of each week `weekly_uniq_hosts`, write to the given file the week number
    and the number of the unique hosts in the corresponding week. The week
    must be sorted in ascending order from smallest to biggest. See the
    print-format below:

    Weekly Number of Unique Hosts
    Week 26: 9413
    Week 27: 32509
    ...
    '''
    # +++your code here+++


def print_status_404_requests(file_report, status_404_requests):
    '''Given the path of a report file `file_report` and all the unique
    404-status requests `status_404_requests`, write to the given file all
    these requests in decending order of its frequency (from largest to
    smallest). See the print-format below:

    List of Frequent 404-status Requests
    /pub/winvn/readme.txt
    /pub/winvn/release.txt
    ...
    '''
    # +++your code here+++
