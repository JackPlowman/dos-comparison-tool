from pytest_bdd import scenarios, then, when
from pytest_bdd.parsers import parse
from requests.models import Response

from ...utils.constants import SYMPTOM_DISCRIMINATORS_URL
from ...utils.utils import api_gateway_request

scenarios("../../features/data/symptom_discriminators.feature")


@when(
    parse('I search for a symptom discriminators with symptom group id "{symptom_group_id:d}"'),
    target_fixture="response",
)
def _(symptom_group_id: int) -> Response:
    """I search for a symptom discriminator."""
    return api_gateway_request(path=f"{SYMPTOM_DISCRIMINATORS_URL}/{symptom_group_id}")


@then("I should see symptom discriminators search results")
def _(response: Response):
    """I should see the symptom discriminators search results.

    Args:
        response (Response): Response from the API Gateway.
    """
    response_json: list[dict] = response.json()
    assert response_json[0]["SymptomDiscriminatorId"] == 4003, "Symptom Discriminator Id is not correct"
    assert (
        response_json[0]["SymptomDiscriminatorName"] == "PC full Primary Care assessment and prescribing capability"
    ), "Symptom Discriminator Name is not correct"


@then("I shouldn't see any symptom discriminators search results")
def _(response: Response):
    """I shouldn't see any symptom discriminators search result.

    Args:
        response (Response): Response from the API Gateway.
    """
    response_json: list[dict] = response.json()
    assert not response_json, "Symptom Discriminators search result is not empty"
