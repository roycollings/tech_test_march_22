"""
Generic utilities that could be common in any other code.
"""
import json
import os
from typing import List
from urllib.parse import urlencode, urlunsplit
from os.path import isfile
from behave.runner import Context

API_VERSION = os.environ["API_VERSION"]
API_URL = os.environ["API_URL"]


# pylint: disable=too-few-public-methods
class ApiType:
    """The different types of api available"""
    public = "public"
    private = "private"


def build_path(api_type: ApiType, endpoint: str) -> str:
    """Creates the 'path' part of the api url."""
    return f"/{API_VERSION}/{api_type}/{endpoint}"


def build_url(path: str, query: str = "", fragment: str = "") -> str:
    """Creates the entire url for our endpoint."""
    scheme = API_URL.split(":")[0]
    domain = API_URL.replace(f"{scheme}://", "")

    return urlunsplit((
        scheme, domain, path, urlencode(query), fragment
    ))


def get_invalid_attribute_values(context: Context, actual: object, expected: object) -> List[str]:
    """Returns an array of failed attribute tests."""
    # Avoids loss of test coverage: always report *all* failures.
    failures = []
    for row in context.table:
        key = row['attribute']
        actual_value = actual[key]
        expected_value = expected[key]
        if actual_value != expected_value:
            failures.append({
                "key": key,
                "expected value": expected_value,
                "actual value": actual_value
            })

    return failures


def get_schema(context: Context) -> object:
    """Gets the relevant json schema for our endpoint."""
    schema_path = f"./features/steps/schemas/{context.endpoint}.json"

    if not isfile(schema_path):
        raise Exception(f"Cannot find schema file '{schema_path}'")

    with open(schema_path, encoding="utf-8") as schema_file:
        return json.load(schema_file)
