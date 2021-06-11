Feature: Manager reimbursement review

    Managers can view all reimbursements past and pending

    Scenario: Navigate to reimbursements page
        Given the manager is logged into the manager portal
        When the view reimbursements button is clicked
        Then the browser navigates to the view reimbursements page

    Managers can appove or deny any reimbursement

    Scenario: View single reimbursement
        Given the manager is viewing the reimbursement requests page
        When the reimbursement is clicked
        Then the browser displays reimbursement details

    Scenario Outline: Actions
        Given the manager is viewing the reimbursement requests page
        When the manager clicks the <action> button
        Then the request is marked <decision> in the database
        And the approve button displays a <mark> mark

        Examples:
            | action  | decision | mark  |
            | approve | approved | check |
            | deny    | denied   | cross |
