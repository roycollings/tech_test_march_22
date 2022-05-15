@public
Feature: Time

  @fixture.schemas
  Scenario: Successful response has a correct schema
    Given I request the server time
    When the request is successful
    Then the response has the correct schema

  # NOTE: can be avoided by excluding @slow tags with TAGS="~@slow".
  @slow
  Scenario: Server time in response increases as time moves on
    Given I request the server time
    And I record the response
    And I wait for "2" seconds
    When I request the server time
    Then the server time has moved forward
