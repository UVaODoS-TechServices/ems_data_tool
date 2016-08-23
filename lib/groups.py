# -*- coding: utf-8 -*-

""" Core data processing routines for EMS Data Tool. """

import json

def process_organizations(items, config):
    """ Preprocesses organization data for insertion into EMS. """

    results = {}
    organizations, memberships = items

    if len(memberships) == 0:
        return

    for organization in organizations:
        orgid = organization['organizationId']
        typename = organization['typeName']
        name = organization['name'][:50]

##        if orgtype not in [value for key, value in type_ids.iteritems()]:
##            continue

        if orgid not in results.keys():
            results[orgid] = {}

        if "GroupName" not in results[orgid].keys():
            results[orgid]['GroupName'] = name

        if "GroupType" not in results[orgid].keys():
            results[orgid]['GroupType'] = typename

    for membership in memberships:
        orgid = membership['organizationId']
        position = membership['positionTemplateName']
        email = membership['userCampusEmail'][:75].lower()
        fname = membership['userFirstName'][:50]
        lname = membership['userLastName'][:50]
        pnumber = email.split('@')[0][:50]

        if orgid not in results.keys():
            continue

##        if "Event Requester" not in position:
##            continue

##        if position in results[orgid].keys():
##            continue

        results[orgid][position] = {"PersonnelNumber": pnumber, \
                                    "FirstName": fname, \
                                    "LastName": lname, \
                                    "MiddleInitial": "", \
                                    "EMailAddress": email, \
                                    "Phone": "", \
                                    "Fax": "", \
                                    "Address1": "", \
                                    "Address2": "", \
                                    "City": "", \
                                    "State": "", \
                                    "ZipCode": "", \
                                    "Country": "", \
                                    "NetworkID": pnumber}

    return results


def process_departments(items, config):
    """ Preprocesses department data for insertion into EMS. """

    results = {}

    departments = items
    mappings = json.loads(config.get("KEYS", "mappings"))

    for department in departments:
        temp = dict.fromkeys((value for key, value in mappings.iteritems()))
        temp['Title'] = department['Title']

        for key, value in department.iteritems():
            if key == 'Title':
                continue

            temp[mappings[key]] = department[key]

        # ignore non-requesters
        if temp['Title'] is None:
            continue

        if "Event Requester" not in temp['Title']:
            if temp['Title'] == "Requester 1":
                temp['Title'] = "Event Requester 1"

            elif temp['Title'] == "Requester 2":
                temp['Title'] = "Event Requester 2"

            else:
                continue


        # check for nulls

        if all([value is None for key, value in temp.iteritems()]):
            continue

        # extract computing id

        pnumber = temp['EMailAddress'].split('@')[0][:50]

        # begin truncation

        orgid = temp['GroupID']
        fname = temp['FirstName']
        lname = temp['LastName']
        position = temp['Title']
        email = temp['EMailAddress'][:75].lower()
        typename = temp['GroupType']
        name = temp['GroupName'][:50]

        if orgid not in results.keys():
            results[orgid] = {}

        if "GroupName" not in results[orgid].keys():
            results[orgid]['GroupName'] = name

        if "GroupType" not in results[orgid].keys():
            results[orgid]['GroupType'] = typename

        if "Event Requester" not in position:
            continue

        if position in results[orgid].keys():
            continue

        results[orgid][position] = {"PersonnelNumber": pnumber, \
                                    "FirstName": fname, \
                                    "LastName": lname, \
                                    "MiddleInitial": "", \
                                    "EMailAddress": email, \
                                    "Phone": "", \
                                    "Fax": "", \
                                    "Address1": "", \
                                    "Address2": "", \
                                    "City": "", \
                                    "State": "", \
                                    "ZipCode": "", \
                                    "Country": "", \
                                    "NetworkID": pnumber}

    return results


if __name__ == "__main__":
    pass
