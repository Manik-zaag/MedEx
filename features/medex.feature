Feature: Retrieve Generic Text from MedEx

  Scenario: Fetch generic information for ACI Limited
    Given I navigate to the MedEx Companies page
    When I click on each company name
    And I view all brands if available
    And I click on each brand
    Then I should retrieve the required information for each brand