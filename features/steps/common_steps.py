"""
Steps that can be used by both private and public scenarios.
"""
# pylint: disable=function-redefined
# pylint: disable=missing-function-docstring

import time
from behave import given, when, then  # pylint: disable=no-name-in-module
from assertpy.assertpy import assert_that
from jsonschema import Draft7Validator

from support import utils


@given('I record the response')
def step_imp(context):
    context.response_previous = context.response


@given('I wait for "{seconds:d}" seconds')
def step_impl(_, seconds):
    time.sleep(seconds)


@when('the request is successful')
def step_impl(context):
    """
    Arguably a 'test' step not an 'action' step, but if this check fails there's no point
    continuing.
    """
    assert_that(context.response.status_code).is_equal_to(200)


@then('the response has the correct schema')
def step_impl(context):
    schema = utils.get_schema(context)
    validator = Draft7Validator(schema)

    errors = validator.iter_errors(context.response.json())

    fails = []
    for error in errors:
        fails.append(f"{error.message}: {error.absolute_schema_path}")

    assert_that(fails).is_equal_to([])


@then('response error is invalid "{expected}"')
def step_impl(context, expected):
    error = context.response.json()['error'][0]
    assert_that(error).contains(f"Invalid {expected}")
