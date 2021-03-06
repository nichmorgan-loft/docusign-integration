import pytest
from docusign_integration.api import BaseApi
from docusign_integration.api import EnvelopeApi
from docusign_integration.models.auth import AuthParams


def test_get_user_info(auth_params: AuthParams):
    api = BaseApi(auth_params)
    user_info = api.get_user_info()

    assert user_info.get("sub") is not None


def test_from_session(auth_params: AuthParams):
    auth_api = BaseApi(auth_params)
    envelop_api = EnvelopeApi(auth_params)

    assert isinstance(BaseApi.from_session(envelop_api), BaseApi)
    assert isinstance(EnvelopeApi.from_session(auth_api), EnvelopeApi)

    with pytest.raises(TypeError):
        EnvelopeApi.from_session(auth_api.__dict__)
