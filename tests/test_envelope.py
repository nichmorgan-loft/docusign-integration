from docusign_integration.api.envelope import EnvelopeApi
import pytest
from os import getenv


@pytest.mark.skip_by_env("BASE_URL", "ENVELOP_ID", "ACCOUNT_ID")
def test_get_envelope_data(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.get_envelope_data(
        getenv("ACCOUNT_ID"), getenv("ENVELOP_ID")
    )
    assert envelope_data is not None
