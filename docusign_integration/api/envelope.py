from docusign_integration.models.response.envelope import EnvelopeDataResponse
from docusign_integration.api import BaseApi
from urllib.parse import urljoin


class EnvelopeApi(BaseApi):
    def get_envelope_data(
        self, account_id: str, envelope_id: str
    ) -> EnvelopeDataResponse:
        url = urljoin(
            self.base_url, f"v2.1/accounts/{account_id}/envelopes/{envelope_id}"
        )
        response = self.get(url)
        response.raise_for_status()

        return EnvelopeDataResponse(**response.json())
