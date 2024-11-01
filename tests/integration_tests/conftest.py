import pytest
from actual import Actual
from actual.queries import create_account


@pytest.fixture
def actual():
    with Actual(
        base_url="http://localhost:12012",
        password="test",
        bootstrap=True,
    ) as actual:
        actual.create_budget("TestBudget")
        actual.upload_budget()
        acc = create_account(actual.session, "TestAccount")
        actual.commit()
        yield actual
        acc.delete()
        actual.delete_budget()
        actual.commit()
