from docusign_integration.api import AuthApi
from docusign_integration.api import EnvelopeApi
from docusign_integration.models.auth import AuthParams


def test_get_user_info(auth_params: AuthParams):
    api = AuthApi(auth_params)
    user_info = api.get_user_info()

    assert user_info.sub is not None


def test_from_session(auth_params: AuthParams):
    auth_api = AuthApi(auth_params)
    envelop_api = EnvelopeApi.from_session(auth_api)

    assert isinstance(auth_api, AuthApi)
    assert isinstance(envelop_api, EnvelopeApi)
