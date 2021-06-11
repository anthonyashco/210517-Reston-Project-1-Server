Feature: Employee reimbursement requests

    Employees can login to see their own reimbursements, past and pending

    Scenario: Navigate to reimbursements page
        Given the employee is logged into the employee portal
        When the view reimbursements button is clicked
        Then the browser navigates to the view reimbursements page

    Employees can submit a reimbursement with an amount and a reason
    Bonus allow for file upload

    Scenario: Navigate to request reimbursement
        Given the employee is logged into the employee portal
        When the request reimbursement button is clicked
        Then the browser navigates to the request reimbursement page

    Scenario: Request reimbursement
        Given the employee is viewing the request reimbursement page
        When the employee fills out the "title"
        And the employee fills out the "amount"
        And the employee fills out the "description"
        And the employee clicks submit
        Then the reimbursement request is saved in the database
        And the employee sees a confirmation message

# Ahoy matey! View reimbursements

#     An employee can login to see their own reimbursements, past and pending

#     Heave to Navigate to reimbursements page
#         Gangway! an employee is logged into the employee portal
#         Blimey! the view reimbursements button is clicked
#         Let go and haul the browser navigates to the reimbursements page

# Pretty much: View reimbursements

#     An employee can login to see their own reimbursements, past and pending

#     Awww, look mate: Navigate to reimbursements page
#         Y'know an employee is logged into the employee portal
#         It's just unbelievable the view reimbursements button is clicked
#         But at the end of the day I reckon the browser navigates to the reimbursements page
