"""
This testing suite is built with help from wonderful
FASTApi test suite documentation
https://fastapi.tiangolo.com/tutorial/testing/
"""

from main import app
from database.mongodb import MongoAPI
from fastapi.testclient import TestClient
from utils.utils import BASEURL, random_string_generator


client = TestClient(app)


def test_service_heart_beat():
    """
    This test checks the API for availability endpoint
    :return:
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_encode():
    """
    This test encodes a given URL to a shortened URL and returns HTTP 200
    :return:
    """
    url = "https://www.facebook.com/"
    response = client.post(f"/encode?url={url}")
    assert response.status_code == 200
    MongoAPI().delete({"url": url})


def test_encode_wrong_url():
    """
    This test encodes incomplete urls, with missing schemes, malformed top
    level domains or missing prefixes
    :return:
    """
    response_incomplete_url = client.post("/encode?url=www.google.com")
    response_malformed_url = client.post("/encode?url=www.google.cpu")
    response_missing_prefix = client.post("/encode?url=google.com")

    assert (
        response_incomplete_url.status_code == 422
        and response_malformed_url.status_code == 422
        and response_missing_prefix.status_code == 422
    )
    assert response_incomplete_url.json() == {"message": "URL not provided / valid"}


def test_encode_same_url_multiple_times():
    """
    This test tries to encode the same URL twice and gets HTTP 400
    error as the URL is already existent in the database
    :return:
    """
    url = "https://www.facebook.com/"
    first_encode_response = client.post(f"/encode?url={url}")
    assert first_encode_response.status_code == 200
    second_encode_response = client.post(f"/encode?url={url}")
    assert second_encode_response.status_code == 400
    MongoAPI().delete({"url": url})


def test_decode_invalid_base_url():
    """
    This test decodes a wrong baseurl which returns HTTP 422 error
    :return:
    """
    response = client.get("/decode?url=https://www.google.com/")
    assert response.status_code == 422
    assert response.json() == {"message": "URL not provided / valid"}


def test_decode_url_not_present():
    """
    This test decodes an unknown URL which returns HTTP 400 error
    :return:
    """
    random_string = random_string_generator()
    response = client.get(f"/decode?url={BASEURL}/{random_string}")
    assert response.status_code == 400
    assert response.json() == {"message": "URL not present in the database"}
