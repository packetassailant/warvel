# warvel

## Objective
```
Wardial Tool: Warvox2 data extraction tool necessary to obtain call details from the PostgreSQL database
```


## Usage
```
$ python warvel.py -h
Info: Warvel was created by Chris Patten
Info: Warvox2 was created by HD Moore
Purpose: Warvox2 database extraction tool
Contact: cpatten[a.t.]packetresearch.com and @packetassailant

Usage: ./warvel.py <options>
Example: ./warvel.py --project=project_name --modem

-u or --usage    Print this help menu
-v or --version  Print the version number
--project        Enter warvox project name (required)
--fax            Extract the detected fax info
--modem          Extract the detected modem info
--voice          Extract the detected voice info
--voicemail      Extract the detected voicemail info
--all            Extract all the info (default)
--json           Output in JSON format
--csv            Output in CSV format (default)
```

## Installation
```
Installation
---------------------------------------------------
Warvel was tested on Ubuntu 12.04 and OSX Mavericks
----------- OSX -----------------------------------
OSX Deps: pip install -U -r environment.txt
----------- Linux ---------------------------------
Linux: sudo apt-get install python-pip
Linux Deps: pip install -U -r environment.txt
```

## Sample Run - CSV Output
```
$ python warvel.py --project=COMPANY_RETAIL --modem
15555555551,modem
15555555552,modem
15555555553,modem
15555555554,modem
15555555555,modem
15555555556,modem
15555555557,modem
15555555558,modem
15555555559,modem
15555555550,modem

```

## Sample Run - JSON Output
```
$ python warvel.py --project=COMPANY_RETAIL --modem --json
{
  "15555555551":"modem",
  "15555555552":"modem",
  "15555555553":"modem",
  "15555555554":"modem",
  "15555555555":"modem",
  "15555555556":"modem",
  "15555555557":"modem",
  "15555555558":"modem",
  "15555555559":"modem",
  "15555555550":"modem"
}

```

## Developing
```
Alpha code under active development
```

## Contact
```
# Author: Chris Patten
# Contact (Email): cpatten[t.a.]packetresearch[t.o.d]com
# Contact (Twitter): packetassailant
```