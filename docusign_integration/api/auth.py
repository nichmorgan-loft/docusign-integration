from typing import Type
from docusign_integration.models.response.user import UserInfoResponse
from docusign_integration.models.auth import AuthParams
from requests_oauthlib.oauth2_session import OAuth2Session
from urllib.parse import urlparse, urljoin


class AuthApi(OAuth2Session):
    _base_url: str

    def __init__(self, data: AuthParams) -> None:
        urlparsed = urlparse(data.refresh_url)
        self._base_url = f"{urlparsed.scheme}://{urlparsed.netloc}"

        OAuth2Session.__init__(
            self,
            client_id=data.client_id,
            token={
                "access_token": data.access_token,
                "refresh_token": data.refresh_token,
                "token_type": "Bearer",
            },
            scope=data.scope,
            auto_refresh_url=data.refresh_url,
            auto_refresh_kwargs={
                "client_secret": data.client_secret,
            },
        )

    @classmethod
    def from_session(cls: Type["AuthApi"], session: Type["AuthApi"]) -> Type["AuthApi"]:
        if not isinstance(session, OAuth2Session):
            raise TypeError(f"session must be a OAuth2Session, not {type(session)}")

        data = AuthParams(
            refresh_url=session.auto_refresh_url,
            client_id=session.client_id,
            client_secret=session.auto_refresh_kwargs.get("client_secret"),
            scope=session.scope,
            access_token=session.token.get("access_token"),
            refresh_token=session.token.get("refresh_token"),
        )
        return cls(data)

    @property
    def base_url(self) -> str:
        return self._base_url

    def get_user_info(self) -> UserInfoResponse:
        response = self.get(url=urljoin(self.base_url, "oauth/userinfo"))
        response.raise_for_status()
        return UserInfoResponse(**response.json())
