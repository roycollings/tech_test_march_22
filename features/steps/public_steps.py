"""
Steps specific to public scenarios.
"""
# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring

import re
import requests
from behave import given, when, then  # pylint: disable=no-name-in-module
from behave.runner import Context
from assertpy.assertpy import assert_that

from support import utils


def fetch_asset_pair(pair: str) -> requests.Response:
    """Returns the reponse from request for this asset pair."""
    endpoint = "AssetPairs"
    query = {"pair": pair}
    path = utils.build_path(utils.ApiType.public, endpoint)
    url = utils.build_url(path, query)
    return requests.get(url)


def expected_attributes_asset_pairs(context: Context) -> object:
    """Returns the asset pair expected attributes"""
    # Some asssets have a suffix, but not all.
    asset1, asset2 = {
        "XXBTZUSD": ["XBT", "USD"]
    }[context.pair]

    asset2_with_suffix = re.sub(f"^.*{asset1}", '', context.pair)
    asset1_with_suffix = re.sub(f"{asset2_with_suffix}$", '', context.pair)

    return {
        "altname": asset1 + asset2,
        "wsname": f"{asset1}/{asset2}",
        "base": asset1_with_suffix,
        "quote": asset2_with_suffix
    }


def actual_attributes_asset_pairs(context: Context) -> object:
    """Returns the asset pair attributes from the response."""
    return context.response.json()["result"][context.pair]


@given('I request details of "{pair}" asset pairs')
def step_impl(context, pair):
    context.endpoint = "AssetPairs"
    context.pair = pair
    context.response = fetch_asset_pair(pair)


@given('I request the server time')
@when('I request the server time')
def step_impl(context):
    context.endpoint = "Time"
    path = utils.build_path(utils.ApiType.public, context.endpoint)
    url = utils.build_url(path)
    context.response = requests.get(url)


@then('the response contains asset pair values for')
def step_impl(context):
    actual = actual_attributes_asset_pairs(context)
    expected = expected_attributes_asset_pairs(context)

    failures = utils.get_invalid_attribute_values(context, actual, expected)

    assert_that(failures).is_equal_to([])


@then('the response includes the asset pair details')
def step_impl(context):
    response = context.response.json()
    pair_properties = response["result"][context.pair]

    assert_that(len(pair_properties.keys())).is_greater_than(0)


@then('the server time has moved forward')
def step_impl(context):
    previous_result = context.response_previous.json()["result"]
    previous_unixtime = previous_result["unixtime"]
    previous_rfc1123 = previous_result["rfc1123"]

    new_result = context.response.json()["result"]
    new_unixtime = new_result["unixtime"]
    new_rfc1123 = new_result["rfc1123"]

    failures = []
    if new_unixtime <= previous_unixtime:
        failures.append({
            "new_unixtime": new_unixtime,
            "previous_unixtime": previous_unixtime
        })

    # (NOTE: If I had more time I'd resolve checking this part of the date was > than previous.)
    if new_rfc1123 == previous_rfc1123:
        failures.append({
            "new_rfc1123": new_rfc1123,
            "previous_rfc1123": previous_rfc1123
        })

    assert_that(failures).is_equal_to([])
