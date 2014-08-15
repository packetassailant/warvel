#!/usr/bin/env python2.7
# Coding: utf-8 
# Project Name: Warvel
# Purpose: Warvox2 database extraction tool
# Author: Chris Patten
# Contact (Email): cpatten[t.a.]packetresearch[t.o.d]com
# Contact (Twitter): packetassailant
#
# Installation
# ---------------------------------------------------
# Warvel was tested on Ubuntu 12.04 and OSX Mavericks
# ----------- OSX -----------------------------------
# OSX Deps: pip install -U -r environment.txt
# ----------- Linux ---------------------------------
# Linux: sudo apt-get install python-pip
# Linux Deps: pip install -U -r environment.txt

import getopt
import psycopg2
import sys
import json

# Constant Declaration
VERSION = "0.1"

# Start of Function Definitions
def usage():
    print 'Info: Warvel was created by Chris Patten'
    print 'Info: Warvox2 was created by HD Moore'
    print 'Purpose: Warvox2 database extraction tool'
    print 'Contact: cpatten[a.t.]packetresearch.com and @packetassailant\n'
    print 'Usage: ./warvel.py <options>'
    print 'Example: ./warvel.py --project=project_name --modem\n'
    print '-u or --usage    Print this help menu'
    print '-v or --version  Print the version number'
    print '--project        Enter warvox project name (required)'
    print '--fax            Extract the detected fax info'
    print '--modem          Extract the detected modem info'
    print '--voice          Extract the detected voice info'
    print '--voicemail      Extract the detected voicemail info'
    print '--all            Extract all the info (default)'
    print '--json           Output in JSON format'
    print '--csv            Output in CSV format (default)'


def initDbConn():
    conn = None
    conn = psycopg2.connect(
        database="warvox",
        # Add DB Connect Creds Below
        user="",
        password="",
        host="127.0.0.1",
        port="5433"
    )
    return conn

def getProjectId(conn, project):
    cur = conn.cursor()
    cur.execute("SELECT id FROM projects WHERE name ILIKE '{0}'".format(project))
    pid = cur.fetchone()
    return pid[0], cur

def getModems(pid, cur):
    cur.execute("SELECT number,line_type FROM lines WHERE project_id={0} AND line_type='modem'".format(pid))
    rows = cur.fetchall()
    return rows

def getVoice(pid, cur):
    cur.execute("SELECT number,line_type FROM lines WHERE project_id={0} AND line_type='voice'".format(pid))
    rows = cur.fetchall()
    return rows

def getFax(pid, cur):
    cur.execute("SELECT number,line_type FROM lines WHERE project_id={0} AND line_type='fax'".format(pid))
    rows = cur.fetchall()
    return rows

def getVoicemail(pid, cur):
    cur.execute("SELECT number,line_type FROM lines WHERE project_id={0} AND line_type='voicemail'".format(pid))
    rows = cur.fetchall()
    return rows

def getAll(pid, cur):
    cur.execute("SELECT number,line_type FROM lines WHERE project_id={0}".format(pid))
    rows = cur.fetchall()
    return rows

def getCSV(rows):
    for row in rows:
        print "{0},{1}".format(row[0], row[1])

def getJSON(rows):
    jstr = json.dumps(dict(rows))
    jdict = json.loads(jstr)
    jobj = json.dumps(jdict, sort_keys=True, indent=2, separators=(',', ':')) 
    print jobj

def main():

    csvFlag = False
    jsonFlag = False
    projectFlag = False
    modemFlag = False
    voiceFlag = False
    faxFlag = False
    voicemailFlag = False
    allFlag = False


# Bootstrap
    try:
        conn = initDbConn()
        opts, args = getopt.getopt(sys.argv[1:], 'uv', ['usage',
                                                        'version',
                                                        'project=',
                                                        'fax',
                                                        'modem',
                                                        'voice',
                                                        'voicemail',
                                                        'all',
                                                        'csv',
                                                        'json',
                                                        ])
        if len(opts) == 0:
            usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-u", "--usage"):
                usage()
                sys.exit(2)
            if opt in ("-v", "--version"):
                print 'Version: {0}'.format(VERSION)
                sys.exit(2)
            if opt == '--project':
                projectFlag = True
                project = arg
            if opt == '--fax':
                faxFlag = True
            if opt == '--modem':
                modemFlag = True
            if opt == '--voice':
                voiceFlag = True
            if opt == '--voicemail':
                voicemailFlag = True
            if opt == '--all':
                allFlag = True
            if opt == '--csv':
                csvFlag = True
            if opt == '--json':
                jsonFlag = True
        if (csvFlag and jsonFlag):
            print "Error: mutually exclusive -- use either the '--csv' or '--json' options\n"
            usage()
            sys.exit(2)
        if not projectFlag:
            print "Error: The Warvox project name is required\n"
            usage()
            sys.exit(2)
        if (allFlag and faxFlag) or \
            (allFlag and modemFlag) or \
            (allFlag and voiceFlag) or \
            (allFlag and voicemailFlag):
            print "Error: mutually exclusive -- the '--all' option cannot be used with other options\n"
            usage()
            sys.exit(2)
        if (faxFlag is False) and \
            (modemFlag is False) and \
            (voiceFlag is False) and \
            (voicemailFlag is False):
            allFlag = True
        if (csvFlag is False) and \
            (jsonFlag is False):
            csvFlag = True
        pid, cur = getProjectId(conn, project)
        if faxFlag:
            rows = getFax(pid, cur)
            if csvFlag:
                getCSV(rows)
            else:
                getJSON(rows)
        if modemFlag:
            rows = getModems(pid, cur)
            if csvFlag:
                getCSV(rows)
            else:
                getJSON(rows)
        if voiceFlag:
            rows = getVoice(pid, cur)
            if csvFlag:
                getCSV(rows)
            else:
                getJSON(rows)
        if voicemailFlag:
            rows = getVoicemail(pid, cur)
            if csvFlag:
                getCSV(rows)
            else:
                getJSON(rows)
        if allFlag:
            rows = getAll(pid, cur)
            if csvFlag:
                getCSV(rows)
            else:
                getJSON(rows)
    except (psycopg2.DatabaseError) as e:
        print 'Error %s' % e
        sys.exit(1)
    except (getopt.GetoptError) as e:
        usage()
        sys.exit(2)
    finally:
        if conn:
            conn.close()

# Code Entry
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating execution"
        sys.exit(0)
