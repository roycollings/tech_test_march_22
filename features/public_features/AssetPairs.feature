@public
Feature: AssetPairs

  @fixture.schemas
  Scenario: Successful response has a correct schema
    Given I request details of "XXBTZUSD" asset pairs
    When the request is successful
    Then the response has the correct schema

  Scenario: Successful response contains pair details
    Given I request details of "XXBTZUSD" asset pairs
    When the request is successful
    Then the response includes the asset pair details

  Scenario: Successful response has predictable asset attributes
    Given I request details of "XXBTZUSD" asset pairs
    When the request is successful
    Then the response contains asset pair values for
      | attribute |
      | altname   |
      | wsname    |
      | base      |
      | quote     |
