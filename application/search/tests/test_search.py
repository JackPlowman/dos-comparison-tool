from functools import partial
from json import dumps
from unittest.mock import MagicMock, call, patch

from aws_lambda_powertools.shared.json_encoder import Encoder
from aws_lambda_powertools.utilities.typing.lambda_context import LambdaContext

from application.search.ccs_comparison_search.ccs_exceptions import CCSAPIResponseError
from application.search.search import lambda_handler

# Fixtures that can't be found in this file are in the conftest.py file
FILE_PATH = "application.search.search"
URL_PATH = "/search/CCSComparisonSearch"
HTTP_METHOD = "POST"
SERIALIZER = partial(dumps, separators=(",", ":"), cls=Encoder)


def test_lambda_handler_invalid_route(lambda_context: LambdaContext) -> None:
    """Test lambda handler with an invalid route.

    Args:
        lambda_context (LambdaContext): Lambda context for search lambda.
    """
    # Arrange
    event = {"body": "invalid", "path": URL_PATH, "httpMethod": "GET"}
    # Act
    response = lambda_handler(event, lambda_context)
    # Assert
    assert response["body"] == SERIALIZER({"statusCode": 404, "message": "Not found"})


@patch(f"{FILE_PATH}.CheckCapacitySummarySearch")
def test_ccs_comparison_search(
    mock_check_capacity_summary_search: MagicMock,
    search_request: dict,
    lambda_context: LambdaContext,
) -> None:
    """Test CCS comparison search.

    Args:
        mock_check_capacity_summary_search (MagicMock): Mocked CheckCapacitySummarySearch.
        search_request (dict): Search request.
        lambda_context (LambdaContext): Lambda context for search lambda.
    """
    # Arrange
    mock_check_capacity_summary_search.return_value.search.return_value = {}
    search_request["path"] = URL_PATH
    search_request["httpMethod"] = HTTP_METHOD
    # Act
    response = lambda_handler(search_request, lambda_context)
    # Assert
    expected_status_code = 200
    assert response["statusCode"] == expected_status_code

    assert response["body"] == SERIALIZER(
        {
            "search_one": {},
            "search_two": {},
            "search_one_environment": "test",
            "search_two_environment": "test2",
        },
    )

    mock_check_capacity_summary_search.assert_has_calls(
        [
            call(
                age=1,
                age_format="years",
                disposition=1,
                symptom_group=1,
                symptom_discriminator_list=[1, 2, 3],
                search_distance=1,
                gender="M",
                search_environment="test",
            ),
            call().search(),
            call(
                age=1,
                age_format="years",
                disposition=1,
                symptom_group=1,
                symptom_discriminator_list=[1, 2, 3],
                search_distance=1,
                gender="M",
                search_environment="test2",
            ),
            call().search(),
        ],
    )


@patch(f"{FILE_PATH}.CheckCapacitySummarySearch")
def test_lambda_handler_with_invalid_request(
    mock_check_capacity_summary_search: MagicMock,
    lambda_context: LambdaContext,
) -> None:
    """Test lambda handler with an invalid request.

    Args:
        mock_check_capacity_summary_search (MagicMock): Mocked CheckCapacitySummarySearch.
        lambda_context (LambdaContext): Lambda context for search lambda.
    """
    # Arrange
    event = {"body": dumps({"test": "tests"}), "path": URL_PATH, "httpMethod": HTTP_METHOD}
    # Act
    response = lambda_handler(event, lambda_context)
    # Assert
    assert response["body"] == SERIALIZER(
        {"message": "Bad Request Error: search_one and search_two are required"},
    )
    mock_check_capacity_summary_search.assert_not_called()


@patch(f"{FILE_PATH}.CheckCapacitySummarySearch")
def test_lambda_handler_ccs_request_error(
    mock_check_capacity_summary_search: MagicMock,
    search_request: dict,
    lambda_context: LambdaContext,
) -> None:
    """Test lambda handler with an internal server error.

    Args:
        mock_check_capacity_summary_search (MagicMock): Mocked CheckCapacitySummarySearch.
        search_request (dict): Search request.
        lambda_context (LambdaContext): Lambda context for search lambda.
    """
    # Arrange
    search_request["path"] = URL_PATH
    search_request["httpMethod"] = HTTP_METHOD
    error_message = "test"
    mock_check_capacity_summary_search.side_effect = CCSAPIResponseError(500, error_code="120", message=error_message)
    # Act
    response = lambda_handler(search_request, lambda_context)
    # Assert
    assert response["body"] == SERIALIZER({"message": f"CCS API Response Error: {error_message}"})


@patch(f"{FILE_PATH}.CheckCapacitySummarySearch")
def test_lambda_handler_internal_server_error(
    mock_check_capacity_summary_search: MagicMock,
    lambda_context: LambdaContext,
) -> None:
    """Test lambda handler with an internal server error.

    Args:
        mock_check_capacity_summary_search (MagicMock): Mocked CheckCapacitySummarySearch.
        lambda_context (LambdaContext): Lambda context for search lambda.
    """
    # Arrange
    event = {"body": "invalid", "path": URL_PATH, "httpMethod": HTTP_METHOD}
    # Act
    response = lambda_handler(event, lambda_context)
    # Assert
    assert response["body"] == SERIALIZER({"statusCode": 500, "message": "Internal Server Error"})
    mock_check_capacity_summary_search.assert_not_called()
