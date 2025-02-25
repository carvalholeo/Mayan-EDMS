from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.sources.tests.mixins.web_form_source_mixins import WebFormSourceBackendTestMixin
from mayan.apps.sources.wizards import DocumentCreateWizardStep

from ..wizard_steps import DocumentCreateWizardStepCabinets

from .mixins import CabinetDocumentUploadWizardStepTestMixin, CabinetTestMixin


class CabinetDocumentUploadTestCase(
    CabinetTestMixin, CabinetDocumentUploadWizardStepTestMixin,
    WebFormSourceBackendTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def tearDown(self):
        super().tearDown()
        DocumentCreateWizardStep.reregister_all()

    def test_upload_interactive_view_with_access(self):
        self._create_test_cabinet()
        self._create_test_cabinet()

        self.grant_access(
            obj=self._test_document_type, permission=permission_document_create
        )
        self.grant_access(
            obj=self._test_source, permission=permission_document_create
        )

        response = self._request_upload_interactive_document_create_view()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self._test_cabinets[0] in Document.objects.first().cabinets.all()
        )
        self.assertTrue(
            self._test_cabinets[1] in Document.objects.first().cabinets.all()
        )

    def test_upload_interactive_cabinet_selection_view_with_access(self):
        DocumentCreateWizardStep.deregister_all()
        DocumentCreateWizardStep.reregister(name=DocumentCreateWizardStepCabinets.name)

        self._create_test_cabinet()
        self.grant_access(
            permission=permission_document_create, obj=self._test_document_type

        )

        response = self._request_wizard_view()
        self.assertEqual(response.status_code, 200)
