from typing import List, Optional, Union
from docusign_integration.models.envelope import (
    IncludeType,
)
from docusign_integration.models.response.envelope import (
    EnvelopeDataResponse,
    EnvelopeListDocumentsResponse,
)
from docusign_integration.api import BaseApi
from urllib.parse import urljoin
import fitz
from pydantic import validate_arguments


class EnvelopeApi(BaseApi):
    @validate_arguments
    def list_envelope_documents(
        self, account_id: str, envelope_id: str
    ) -> EnvelopeListDocumentsResponse:
        """Retrieves a list of documents associated with the specified envelope.

        reference: https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopedocuments/list/

        Args:
            account_id (str)
            envelope_id (str)

        Returns:
            EnvelopeListDocumentsResponse
        """

        url = urljoin(
            self.base_url,
            f"v2.1/accounts/{account_id}/envelopes/{envelope_id}/documents",
        )
        response = self.get(url, stream=True)
        response.raise_for_status()

        return EnvelopeListDocumentsResponse(**response.json())

    @validate_arguments
    def download_envelope_document(
        self, account_id: str, envelope_id: str, document_id: int
    ) -> fitz.Document:
        """Download envelope document into a fitz document (PDF)

        reference: https://developers.docusign.com/docs/esign-rest-api/how-to/download-envelope-documents/

        Args:
            account_id (str)
            envelope_id (str)
            document_id (int)

        Returns:
            fitz.Document
        """

        url = urljoin(
            self.base_url,
            f"v2.1/accounts/{account_id}/envelopes/{envelope_id}/documents/{document_id}",
        )
        response = self.get(url)
        response.raise_for_status()

        return fitz.open("pdf", response.content)

    @validate_arguments
    def get_envelope_data(
        self,
        account_id: str,
        envelope_id: str,
        *,
        advanced_update: Optional[bool] = None,
        include: Optional[List[Union[str, IncludeType]]] = None,
    ) -> EnvelopeDataResponse:
        """Retrieves the overall status for the specified envelope.

        reference: https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopes/get/

        Args:
            params (GetEnvelopeArgs)

        Returns:
            EnvelopeDataResponse
        """

        url = urljoin(
            self.base_url,
            f"v2.1/accounts/{account_id}/envelopes/{envelope_id}",
        )

        query_params = {}
        if advanced_update is not None:
            query_params["advanced_update"] = advanced_update
        if include is not None:
            query_params["include"] = ",".join(include)

        if query_params:
            query_params = query_params.dict(exclude_unset=True, exclude_none=True)
            if "include" in query_params:
                query_params["include"] = ",".join(query_params["include"])

        response = self.get(url, params=query_params)
        response.raise_for_status()

        return EnvelopeDataResponse(**response.json())
