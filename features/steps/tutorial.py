from behave import given, when, then


@given("INSTALL BEHAVE?")
def install_behave(context):
    pass


@when("I TEST")
def i_test(context):
    assert True is not False


@then("BEHAVE DO TEST!")
def behave_do_test(context):
    assert context.failed is False
