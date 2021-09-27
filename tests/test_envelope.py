from docusign_integration.models.envelope import IncludeTypeEnum
import fitz
from docusign_integration.models.response.envelope import (
    EnvelopeDataResponse,
    EnvelopeListDocumentsResponse,
)
from docusign_integration.api.envelope import EnvelopeApi
import pytest
from os import getenv


skip_by_env = pytest.mark.skip_by_env("BASE_URL", "ENVELOP_ID", "ACCOUNT_ID")


@skip_by_env
def test_get_envelope_data(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.get_envelope_data(
        getenv("ACCOUNT_ID"),
        getenv("ENVELOP_ID"),
        advanced_update=False,
        include=[IncludeTypeEnum.CUSTOM_FIELDS],
    )
    assert isinstance(envelope_data, EnvelopeDataResponse)


@skip_by_env
def test_list_envelope_documents(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.list_envelope_documents(
        getenv("ACCOUNT_ID"), getenv("ENVELOP_ID"), only_content=False
    )

    assert isinstance(envelope_data, EnvelopeListDocumentsResponse)
    try:
        EnvelopeListDocumentsResponse.validate(envelope_data)
    except (Exception,) as e:
        pytest.fail("EnvelopeListDocumentsResponse validation fails:\n" + str(e))

    if not envelope_data.has_only_content:
        envelope_data = envelope_api.list_envelope_documents(
            getenv("ACCOUNT_ID"), getenv("ENVELOP_ID"), only_content=True
        )
        assert envelope_data.has_only_content


@skip_by_env
def test_download_envelope_document(envelope_api: EnvelopeApi):
    envelope_data = envelope_api.list_envelope_documents(
        getenv("ACCOUNT_ID"),
        getenv("ENVELOP_ID"),
    )

    assert len(envelope_data.envelopeDocuments) > 0
    document = envelope_data.envelopeDocuments.pop()

    document_file = envelope_api.download_envelope_document(
        getenv("ACCOUNT_ID"), getenv("ENVELOP_ID"), document.documentId
    )

    assert isinstance(document_file, fitz.Document)
