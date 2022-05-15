@private
Feature: OpenOrders

  Scenario: Request with no authentication is rejected
    Given I request OpenOrders with no authentication
    When the request is successful
    Then response error is invalid "arguments"

  Scenario: Request with invalid api key is rejected
    Given I request OpenOrders with an invalid API key
    When the request is successful
    Then response error is invalid "key"

  Scenario: Request with invalid api signature is rejected
    Given I request OpenOrders with an invalid API signature
    When the request is successful
    Then response error is invalid "signature"

  Scenario: Successful response has a correct schema
    Given I request OpenOrders with correct authentication
    When the request is successful
    Then the response has the correct schema
