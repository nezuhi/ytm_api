#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import csv
import urllib.request, urllib.parse, urllib.error
import time
import concurrent.futures
from queue import Queue


logtime = time.strftime('%Y%m%d-%H%M%S')
parser = argparse.ArgumentParser(prog='csv_request_generator', description="This script read header and column data from CSV file then set them in query string parameters of http requests which are sent to YTM Plus API. The key of query string parameter is taken from the header and value is set from column data. Be sure to CSV file contains header and save it in UTF-8! Example: python csv_request_generator.py -f '/path to file.csv' -s 'abc1234' -r 'api:sample' -t 5 -l'", epilog='')
parser.add_argument('-f','--file', dest='csvfile', action='store', type=str, help='Insert path to csv file into CSVFILE.', required=True)
parser.add_argument('-s','--siteid', dest='siteid', action='store', type=str, help='Insert YTM SiteID into SITEID.', required=True)
parser.add_argument('-r','--referrer', dest='referrer', action='store', type=str, help='Insert API Event ID into REFERRER.', required=True)
parser.add_argument('-t','--thread', dest='thread', action='store', const=2, default=1, nargs='?', type=int, choices=list(range(1, 11)), help='Specify the number of concurrent connections. If this option is not specified, default is set to 1. If argument is omitted, simultaneous connecions is set to 2.')
parser.add_argument('-l','--logfile', dest='logfile', action='store', const="./csv_request_" + str(logtime) + ".log", nargs='?', type=str, help='HTTP_CODE, RESPONSE, URL will be written to the logfile if this option is specified. If argument is ommited, csv_request_YYYYMMDD-HHMMSS.log is created in current working directory, otherwise specify the path and the filename of the logfile in argument.')
parser.add_argument('-m','--mode', dest='mode', action='store', const='preview', nargs='?', type=str, choices=['preview', 'diagnostic'], help='Set this option when you want to send the requests in preview mode for confirmation etc. Remember to set the behavior tag in YTM to preview mode as well. If argument is ommited, mode will be set to preview, otherwise specify the mode in argument.')
parser.add_argument('-p','--protocol', dest='protocol', action='store', const='https', default='http', nargs='?', type=str, choices=['http', 'https'], help='Set this option when you want to specify the protocol. Choose from either http or https. If this option is not specified, default is set to http. If argument is omitted, requests will be sent with https.')
parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()
print(args)
####################################################################
def encode_url(str):
    strEncoded = urllib.parse.quote(str)
    return strEncoded


def get_header(csvfile):
    headerColumn = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for i in header:
            headerColumn.append(i)
    return headerColumn


def get_url(csvfile, baseurl, headerColumn):
    column = []
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            for i in row:
                column.append(i)
                params = dict(list(zip(headerColumn,column)))
            parameter = urllib.parse.urlencode(params)
            url = "%s&%s" %(baseurl,parameter)
            column[:] = []
            yield url


def fetch_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.geturl(), conn.getcode(), conn.read().decode('utf-8')


def write_log(log_file, string_format):
    f = open(log_file,'a')
    f.write(string_format)
    f.close()

####################################################################
def main():
    siteid = args.siteid
    referrer = encode_url(args.referrer)
    csvfile = args.csvfile
    threads = args.thread
    time_started = time.time()

    if args.mode:
        baseurl = "%s://s.thebrighttag.com/api?site=%s&referrer=%s&mode=%s" %(args.protocol, siteid, referrer, args.mode)
    else:
        baseurl = "%s://s.thebrighttag.com/api?site=%s&referrer=%s" %(args.protocol, siteid, referrer)

    headerColumn = get_header(csvfile)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_url = {executor.submit(fetch_url, url, 60): url for url in get_url(csvfile, baseurl, headerColumn)}
        count = 0
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                count += 1
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                if args.logfile:
                    string_format = "{{\"requestUrl\":\"{}\",\"statusCode\":{},\"responseText\":\"{}\"}}\n".format(data[0], data[1], data[2])
                    write_log(args.logfile, string_format)
                else:
                    print('%r\t%d\t%r' % (data[0], data[1], data[2]))

    time_completed = time.time()
    time_elapsed = time_completed-time_started
    print("Completed: {} requests in {} seconds".format(str(count),str(time_elapsed)))
    if args.logfile:
        write_log(args.logfile, "{} requests sent in {} senconds".format(str(count), str(time_elapsed)))


if __name__ == "__main__":
    main()
