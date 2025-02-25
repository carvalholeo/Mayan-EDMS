from django.core.exceptions import ValidationError

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.testing.tests.base import BaseTestCase

from ..models import Cabinet

from .literals import TEST_CABINET_LABEL
from .mixins import CabinetTestMixin


class CabinetTestCase(CabinetTestMixin, BaseTestCase):
    def test_cabinet_creation(self):
        self._create_test_cabinet()

        self.assertEqual(Cabinet.objects.all().count(), 1)
        self.assertQuerysetEqual(
            Cabinet.objects.all(), (repr(self._test_cabinet),)
        )

    def test_cabinet_duplicate_creation(self):
        self._create_test_cabinet()

        with self.assertRaises(expected_exception=ValidationError):
            cabinet_2 = Cabinet(label=TEST_CABINET_LABEL)
            cabinet_2.validate_unique()
            cabinet_2.save()

        self.assertEqual(Cabinet.objects.all().count(), 1)
        self.assertQuerysetEqual(
            Cabinet.objects.all(), (repr(self._test_cabinet),)
        )

    def test_inner_cabinet_creation(self):
        self._create_test_cabinet()

        inner_cabinet = Cabinet.objects.create(
            parent=self._test_cabinet, label=TEST_CABINET_LABEL
        )

        self.assertEqual(Cabinet.objects.all().count(), 2)
        self.assertQuerysetEqual(
            Cabinet.objects.all(),
            map(repr, (self._test_cabinet, inner_cabinet))
        )

    def test_method_get_absolute_url(self):
        self._create_test_cabinet()

        self.assertTrue(self._test_cabinet.get_absolute_url())


class CabinetDocumentTestCase(
    CabinetTestMixin, DocumentTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        self._create_test_cabinet()

    def test_addition_of_documents(self):
        self._test_cabinet.documents.add(self._test_document)

        self.assertEqual(self._test_cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            self._test_cabinet.documents.all(), (repr(self._test_document),)
        )

    def test_addition_and_deletion_of_documents(self):
        self._test_cabinet.documents.add(self._test_document)

        self.assertEqual(self._test_cabinet.documents.count(), 1)
        self.assertQuerysetEqual(
            self._test_cabinet.documents.all(), (repr(self._test_document),)
        )

        self._test_cabinet.documents.remove(self._test_document)

        self.assertEqual(self._test_cabinet.documents.count(), 0)
        self.assertQuerysetEqual(self._test_cabinet.documents.all(), ())

    def test_cabinet_get_document_count_method(self):
        self._test_cabinet.documents.add(self._test_document)

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self.assertEqual(
            self._test_cabinet.get_document_count(user=self._test_case_user),
            len(self._test_documents)
        )

    def test_trashed_document_cabinet_document_count_method(self):
        self._test_cabinet.documents.add(self._test_document)
        self._test_document.delete()

        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self.assertEqual(
            self._test_cabinet.get_document_count(user=self._test_case_user),
            len(self._test_documents) - 1
        )
