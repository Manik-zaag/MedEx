Feature: Login functionality on the Sign In page
  As a user
  I want to log in to the application
  So that I can access my account and perform actions

  Background:
    Given I am on the login page

  @login
  Scenario: Owner Sign in with valid credentials
    When I select Owner as login type
    When I enter valid email address and valid password into the fields
      | email              | password |
      | pms_tc11@gmail.com | aA123456 |
    And I click on Log in button
    Then I should get logged in

  @login
  Scenario Outline: Owner Login with unauthorized email and valid password
    When I enter unauthorized email address as "<email>" and valid password as "<password>" into the fields
    And I click on Log in button
    Then I should get a warning message as "Incorrect username or password."
    Examples:
      | email              | password |
      | manik543@gmail.com | aA123456 |

  @login
  Scenario Outline: Owner Login with invalid email and valid password
    When I enter invalid email address as "<email>" and valid password as "<password>" into the fields
    And I click on Log in button
    Then I should get a warning message for invalid email as "The input is not valid E-mail!"
    Examples:
      | email                                                   | password |
      | invalid@.com                                            | aA123456 |
      | invalidemail.com                                        | aA123456 |
      | invalid@domain                                          | aA123456 |
      | invalid@@domain.com                                     | aA123456 |
      | inv@lid@domain.com                                      | aA123456 |
      | inv@lid!domain.com                                      | aA123456 |
      | invalid email@domain.com                                | aA123456 |
      | .invalid@domain.com                                     | aA123456 |
      | invalid@domain.c0m                                      | aA123456 |
      | invalid@domain..com                                     | aA123456 |
      | invalid@thisisaverylongdomainthatexceedsnormalemail.com | aA123456 |


  @login
  Scenario Outline: Owner Login with valid email and invalid password
    When I enter valid email address as "<email>" and invalid password as "<password>" into the fields
    And I click on Log in button
    Then I should get a warning message as "Incorrect username or password."
    Examples:
      | email              | password |
      | pms_tc11@gmail.com | 12345677 |


  @login
  Scenario Outline: Owner Login with valid email and less password character than minimum
    When I enter valid email address as "<email>" and invalid password as "<password>" into the fields
    And I click on Log in button
    Then I should get a warning message as "Incorrect username or password."
    Examples:
      | email              | password |
      | pms_tc11@gmail.com | 123      |

  @login
  Scenario Outline: Owner Login with invalid credentials
    When I enter invalid email address as "<email>" and invalid password as "<password>" into the fields
    And I click on Log in button
    Then I should get a warning message as "Incorrect username or password."
    Examples:
      | email                   | password |
      | amotsampleone@gmail.com | 12347678 |

  @login
  Scenario: Owner Login without entering any credentials
    When I do not enter anything into email address and password fields
    And I click on Log in button
    Then I should get a proper inline warning message as "Please enter your email!" and "Please enter your password!"
