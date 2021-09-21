from docusign_integration.api.envelope import EnvelopeApi
from docusign_integration.models.auth import AuthParams
import pytest
from os import getenv
from urllib.parse import urljoin


@pytest.fixture(scope="session")
def auth_params() -> AuthParams:
    return AuthParams(
        base_url=getenv("AUTHORIZATION_SERVER"),
        refresh_url=f"{getenv('AUTHORIZATION_SERVER')}/oauth/token",
        client_id=getenv("CLIENT_ID"),
        client_secret=getenv("CLIENT_SECRET"),
        refresh_token=getenv("REFRESH_TOKEN"),
        access_token=getenv("ACCESS_TOKEN"),
        scope=getenv("SCOPES", "signature").split(" "),
    )


@pytest.fixture(scope="session")
def envelope_api(auth_params: AuthParams) -> EnvelopeApi:
    auth_params.base_url = urljoin(getenv("BASE_URL"), "/restapi")
    return EnvelopeApi(auth_params)


@pytest.fixture(autouse=True)
def skip_by_env(request):
    if request.node.get_closest_marker(skip_by_env.__name__):
        for key in request.node.get_closest_marker(skip_by_env.__name__).args:
            if getenv(key) is None:
                pytest.skip(f"skipped because the env key '{key}' is required")
