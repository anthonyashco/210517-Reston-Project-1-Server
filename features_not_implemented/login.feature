Feature: users can log into the system.

    Users log in with a username / password pair stored in the database. Based
    on saved information, user is determined to be either an employee or a
    manager and is forwarded to the appropriate interface.

    Scenario Outline: user logs in
        Given the user is on the login page
        When the user inputs their "username"
        And the user inputs their "password"
        And the user clicks submit
        Then the browser navigates to the "userclass" page
