*** Settings ***


Documentation    Tests cases for testing the example migration and seeds

Resource    ../resource/resource.robot

Suite Setup    SuiteSetup

Suite Teardown    SuiteTeardown

Test Teardown    TestTeardown



*** Test Cases ***


Can migrate an empty database to head
    [Documentation]    Tests that migrations can be applied to fresh database
    [Tags]    fresh-db    upgrade    head
    Given an empty database is ready and accepting connections
    When migrate is ran with direction up and revison id head
    Then the database will have a table called accounts
    And the accounts table will have a columns named user_id,username,password,email,created_on,last_login


Can seed an empty database
    [Documentation]    Tests that a database can be seeded
    [Tags]    fresh-db    upgrade    head    seed
    Given an empty database is ready and accepting connections
    And seed enviroment is set
    When migrate is ran with direction upgrade and revison id head
    And the database is seeded
    Then the database will have a table called accounts
    And the accounts table will have 203 records
    And the first record from accounts table will have a value of my username in the username column
    And the first record from accounts table will have a value of myPassword in the password column
    And the first record from accounts table will have a value of my.email@email.com in the email column


Can migrate both directions
    [Documentation]    Tests that migrations can be applied and reverted
    [Tags]    fresh-db    upgrade    downgrade    head    base
    Given an empty database is ready and accepting connections
    And seed enviroment is set
    When migrate is ran with direction upgrade and revison id head
    Then the database will have a table called accounts
    When migrate is ran with direction downgrade and revison id base
    Then the database will NOT have a table called accounts
