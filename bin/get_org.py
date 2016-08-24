#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

from ConfigParser import SafeConfigParser
from requests import Session
from lib.atuva import get_items
from lib.groups import process_organizations
from lib.tools import unpack
from ems_update import get_memberships


def main():
    config = SafeConfigParser()
    config.optionxform(str())
    config.read("config/settings.ini")
    s = Session()
    r = "organizations"
    param = {"status": "active","type": "Contracted Independent Organization"}
    orgs = list()
    for organization in get_items(config, r, param, s):
        m = get_memberships(organization, config, s)
        organization = process_organizations(([organization,],m), config)
        organization = [unpack(organization)]
        orgs.append(organization)

    with open("organization.json", 'w') as fout:
        for org in orgs:
            fout.write(json.dumps(org) + '\n')


if __name__ == "__main__":
    main()

    dict()
    m = ["a","b", "c", ]
    l = dict.fromkeys(m)

