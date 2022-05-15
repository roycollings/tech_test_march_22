"""
Steps specific to private scenarios.
"""
# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring

import time
import hashlib
import hmac
import base64
from os import environ
from urllib.parse import urlencode
import requests
from behave import given  # pylint: disable=no-name-in-module
from behave.runner import Context
from dotenv import load_dotenv

from support import utils

# Load environment variables.
load_dotenv()
KPUBLIC = environ["KPUBLIC"]
KPRIVATE = environ["KPRIVATE"]
KOTP = environ["KOTP"]


def build_signature(urlpath: str, data: object, secret: str) -> str:
    """
    Returns an encoded API signature for these details.

    DISCLOSURE: I couldn't find information on generating this in documentation,
                so this function was copied from a blog (I can give the url on request).
    """
    postdata = urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def set_request_elements(context: Context) -> None:
    """Adds the 'url', 'data' and 'headers' values to the context."""
    path = utils.build_path(utils.ApiType.private, context.endpoint)
    context.url = utils.build_url(path)

    nonce = str(int(time.time()*1000))
    context.data = {"nonce": nonce, "otp": KOTP}

    signature = build_signature(path, context.data, KPRIVATE)
    context.headers = {
        'API-Key': KPUBLIC,
        'API-Sign': signature,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
    }


def fetch_private_response(context: Context) -> requests.Response:
    """Returns the reponse from request with this context's 'url', 'data' and 'headers'."""
    return requests.post(
        url=context.url,
        headers=context.headers,
        data=context.data
    )


@given('I request OpenOrders with no authentication')
def step_impl(context):
    context.endpoint = "OpenOrders"

    set_request_elements(context)
    context.headers = {}
    context.data = {}

    context.response = fetch_private_response(context)


@given('I request OpenOrders with an invalid API key')
def step_impl(context):
    context.endpoint = "OpenOrders"

    set_request_elements(context)
    context.headers['API-Key'] = 'x'

    context.response = fetch_private_response(context)


@given('I request OpenOrders with an invalid API signature')
def step_impl(context):
    context.endpoint = "OpenOrders"

    set_request_elements(context)
    context.headers['API-Sign'] = 'x'

    context.response = fetch_private_response(context)


@given('I request OpenOrders with correct authentication')
def step_impl(context):
    context.endpoint = "OpenOrders"

    set_request_elements(context)

    context.response = fetch_private_response(context)
