Feature: Customer Management

  Scenario: Create a new customer
    Given I submit a new customer data
    Then the customer should be created successfully

  Scenario: Get customer by CPF
    Given there is a customer with a specific CPF
    When I request to get the customer by CPF
    Then I should receive the customer details by CPF

  Scenario: Get customer by ID
    Given there is a customer with a specific ID
    When I request to get the customer by ID
    Then I should receive the customer details by ID

  Scenario: Get all customers
    Given there are existing customers in the system
    When I request to get all customers
    Then I should receive a list of customers

  Scenario: Update customer data
    Given there is a registered customer
    When I request to update a customer
    Then the customer data is successfully updated

  Scenario: Remove a customer
    Given there is a customer on database with specific id
    When I request to remove a customer
    Then the customer data is successfully removed