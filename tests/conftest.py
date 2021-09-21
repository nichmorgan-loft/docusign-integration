from docusign_integration.models.auth import AuthParams
import pytest
from dotenv import load_dotenv
from os import getenv

load_dotenv(".test.env")


@pytest.fixture(scope="session")
def auth_params() -> AuthParams:
    return AuthParams(
        refresh_url=f"{getenv('AUTHORIZATION_SERVER')}/oauth/token",
        client_id=getenv("CLIENT_ID"),
        client_secret=getenv("CLIENT_SECRET"),
        refresh_token=getenv("REFRESH_TOKEN"),
        access_token=getenv("ACCESS_TOKEN"),
        scope=getenv("SCOPES", "signature").split(" "),
    )
