# -*- coding: utf-8 -*-

""" @UVa API Handler for EMS Data Tool. """

import hashlib
import sys
import time
import uuid

from urllib2 import urlparse
from requests import Request, Session

def create_hash(*args):
    """ Hashes a unique value using md5. """

    plaintext = ""
    for arg in args:
        plaintext += arg

    cryptext = hashlib.md5(plaintext).hexdigest()

    return cryptext


def create_random():
    """ Creates a random value using uuid. """

    return uuid.uuid4().hex


def get_current_time():
    """ Gets the current time in milliseconds. """

    return str(int(round(time.time() * 1000)))


def make_request(config, resource, params, session=None, headers=None):
    """ Makes a request to atuva api with params. """

    if headers is None:
        headers = {}

    if session is None:
        session = Session()

    headers['Content-Type'] = "application/json"

    params['apikey'] = config.get("MAIN", "apikey")
    params['ip'] = config.get("MAIN", "ip")
    params['random'] = create_random()
    params['time'] = get_current_time()
    params['hash'] = create_hash(params['apikey'],
                                 params['ip'],
                                 params['time'],
                                 params['random'],
                                 config.get("MAIN", "privatekey"))

    url = config.get("MAIN", "apiurl")
    completeurl = urlparse.urljoin(url, resource)

    request = Request("GET", completeurl, params=params, headers=headers)
    prepared = session.prepare_request(request)
    response = session.send(prepared)

    if not response.ok:
        tries = 3

        while not response.ok:
            if tries == 0:
                sys.stderr.write("number of tries exhausted!\n")
                sys.stderr.flush()
                ##sys.exit(-1)
                return

            response = session.send(prepared)
            tries -= 1
            time.sleep(1)

    return response


def get_items(config, resource, params, session=None, headers=None):
    """ Generator for items from parameters. """

    if headers is None:
        headers = {}

    params['page'] = 1
    response = make_request(config, resource, params, session, headers)

    total = response.json()['totalPages']
    if resource == "organizations":
        message = "{0} has {1} pages total.\n".format(resource, total)

        sys.stderr.write(message)
        sys.stderr.flush()

    results = response.json()['items']

    for result in results:
        yield result

    for _ in xrange(1, (total + 1)):
        params['page'] = 2
        response = make_request(config, resource, params, session, headers)

        for item in response.json()['items']:
            yield item


if __name__ == "__main__":
    pass
