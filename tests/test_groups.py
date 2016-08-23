# -*- coding: utf-8 -*-

""" Unittests for groups library. """

import unittest

from ConfigParser import SafeConfigParser

from lib.groups import process_departments, process_organizations

BOGUS = ("0DDC0FFEE", "BADF00D", "FACED00D", "DEADBEEF", \
         "CAFEBABE")


class TestGroups(unittest.TestCase):
    """ Tests for validating groups library. """

    def test_process_organizations(self):
        """ Tests ability to parse organization data. """

        config = SafeConfigParser()
        config.optionxform(str())
        config.read("./config/settings.ini")

        organization = {"organizationId": BOGUS[0], \
                        "typeId": BOGUS[1], \
                        "name": BOGUS[2], \
                        "typeName": BOGUS[3]}
        membership = {"organizationId": BOGUS[0], \
                      "positionTemplateName": BOGUS[4], \
                      "userCampusEmail": "{0}@{1}.{2}".format( \
                                            BOGUS[0][:3], \
                                            BOGUS[4][:4], \
                                            BOGUS[0][3:5]), \
                      "userFirstName": BOGUS[4][:4], \
                      "userLastName": BOGUS[4][4:]}

        result = process_organizations(([organization], [membership]), config)
        self.assertIsInstance(result, dict)

    def test_process_departments(self):
        """ Tests ability to parse department data. """

        config = SafeConfigParser()
        config.optionxform(str())
        config.read("./config/settings.ini")

        department = {"First Name": BOGUS[4][:4], \
                      "Last Name": BOGUS[4][4:], \
                      "Title": BOGUS[4], \
                      "Email": "{0}@{1}.{2}".format( \
                                  BOGUS[0][:3], \
                                  BOGUS[4][:4], \
                                  BOGUS[0][3:5]), \
                      "Organization #": BOGUS[0], \
                      "Organization Name": BOGUS[2], \
                      "Organization Type": BOGUS[3]}

        result = process_departments([department], config)

        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    pass
