# -*- coding: utf-8 -*-

""" Helper functions for EMS Data Tool. """

import time

from openpyxl import load_workbook

class StatusMessage(object):
    """ Echoes __call__ input if differs from previous __call__. """

    def __init__(self):
        self._message = ""

    def __call__(self, message):
        if message == self._message:
            return None

        self._message = message

        return message


def parse_spreadsheet(file_obj):
    """ Reads in saved data. """

    results = []
    workbook = load_workbook(file_obj, read_only=True)
    worksheet = workbook[workbook.worksheets[0].title]

    for row in worksheet.rows:

        results.append([cell.value for cell in row])

    headers = results[0]
    results = results[1:]

    for row_i, result in enumerate(results):
        temp = dict.fromkeys(headers)

        if len(result) < len(headers):
            continue

        for field_i, field in enumerate(result):
            temp[headers[field_i]] = field

        results[row_i] = temp

    return results


class Timer(object):
    """ Times runtime of object decorated. """

    def __init__(self, obj):
        self._obj = obj

    def __call__(self, *args, **kwargs):
        start = time.time()
        result = self._obj(*args, **kwargs)
        end = time.time()
        elapsed = round(end - start)

        if elapsed == 0.0:
            return result

        try:
            print "%s() completed in %s" % (self._obj.func_name, elapsed)

        except:
            print "completed in %s" % (elapsed)

        return result


def unpack(items):
    """ Generator that converts orgs into requesters for EMS. """

    for orgid, organization in items.iteritems():
        groupname = organization['GroupName']
        grouptype = organization['GroupType']
        for typ in ("Event Requester 1", "Event Requester 2"):
            if typ in organization.keys():
                yield [organization[typ]['NetworkID'], organization[typ]['FirstName'], \
                       organization[typ]['LastName'], typ, organization[typ]['MiddleInitial'], \
                       organization[typ]['EMailAddress'], organization[typ]['Phone'], \
                       organization[typ]['Fax'], organization[typ]['Address1'], \
                       organization[typ]['Address2'], organization[typ]['City'], \
                       organization[typ]['State'], organization[typ]['ZipCode'], \
                       organization[typ]['Country'], organization[typ]['NetworkID'], \
                       orgid, groupname, grouptype]


def pack(items):
    """ Generator that converts requesters into orgs. """

    groups = {}

    for item in items:
        if item[15] not in groups.keys():
            groups[item[15]] = {"GroupName": item[16], "GroupType": item[17]}

        temp = {
            "PersonnelNumber": item[0],
            "FirstName": item[1],
            "LastName": item[2],
            "MiddleInitial": item[4],
            "EMailAddress": item[5],
            "Phone": item[6],
            "Fax": item[7], "Address1": item[8],
            "Address2": item[9],
            "City": item[10],
            "State": item[11],
            "ZipCode": item[12],
            "Country": item[13],
            "NetworkID": item[14]
            }

        if item[3] == "Event Requester 1":
            groups[item[15]]['Event Requester 1'] = temp

        elif item[3] == "Event Requester 2":
            groups[item[15]]['Event Requester 2'] = temp

    for key, value in groups.iteritems():
        yield {key: value}


def create_connmsg(svr, drv, db, un, pwd, tc):
    """ Creates a string that can be used to connect using pyodbc. """

    connmsg = "SERVER={svr};DRIVER={drv};DATABASE={db};"
    connmsg += "UID={un};PWD={pwd};Trusted_Connection={tc};"

    return connmsg.format(svr=svr, drv=drv, db=db, un=un, pwd=pwd, tc=tc)


if __name__ == "__main__":
    pass
