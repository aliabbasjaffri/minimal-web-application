import validators
from database.mongodb import MongoAPI
from fastapi import APIRouter, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from utils.utils import BASEURL, random_string_generator, valid_base_url


router = APIRouter()
# Jinja2Templates requires package jinja2 to be installed
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=JSONResponse)
async def heart_beat_check():
    """
    API can be pinged at this endpoint to test for heart beat status
    :return: HTTP 200 code with message {"message": "Hello World"}
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Hello World"}
    )


@router.get("/hello", response_class=HTMLResponse)
async def hello(request: Request):
    """
    This function returns a default html page for welcoming users
    on /hello route
    :param request: a default request
    :return: a html template for welcoming users
    """
    return templates.TemplateResponse("hello.html", {"request": request})


@router.post("/encode", response_class=JSONResponse)
async def encode(url: str):
    """
    This function shortens a given URL.
    The url is first checked for validations regarding none value, or valid correct
    url or has the user passed an already shortened url.
    Next, it checks if the URL already exists in the database. If so, it returns
    an error message. Otherwise, it proceeds to generate a random string for the
    provided URL and then stores it in
    :param url: URL to be shortened
    :return: returns a shortened url
    """
    url = url.strip()

    if url is None or not validators.url(url) or valid_base_url(url):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "URL not provided / valid"},
        )

    # TODO: random string function can be replaced by a hash generator

    mongodb_api = MongoAPI()

    if mongodb_api.find({"url": url}):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "URL already present in the database"},
        )

    random_string = random_string_generator()
    shortened_url = BASEURL + random_string

    mongodb_api.insert(data={"url": url, "shortened_url": shortened_url})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": f"Shortened URL: {shortened_url}"},
    )


@router.get("/decode", response_class=JSONResponse)
async def decode(url: str):
    """
    This function decodes a given URL by extracting the random string.
    The url is first checked for validations.
    Next, the random string is extracted from the URL, if the random string exists in the
    database, the url is looked up against it, otherwise an error message is returned.
    and then looking up that string in the database and returning it
    :param url: generated url with BASEURL as main URL followed by a generated random string
    :return: JSONResponse with original URL stored in the database against the random string
    """
    url = url.strip()

    if url is None or not validators.url(url) or not valid_base_url(url):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "URL not provided / valid"},
        )

    mongodb_api = MongoAPI()

    if mongodb_api.find({"shortened_url": url}):
        data = mongodb_api.read({"shortened_url": url})
        original_url = data["url"]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Original URL: {original_url}"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "URL not present in the database"},
        )
