"""Configuration options for the documents app"""

import datetime
import hashlib
import uuid

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from common.utils import proper_name
from storage.backends.filebasedstorage import FileBasedStorage
from main.api import register_settings


def default_checksum(x):
    """hashlib.sha256(x).hexdigest()"""
    return hashlib.sha256(x).hexdigest()


def default_uuid():
    """unicode(uuid.uuid4())"""
    return unicode(uuid.uuid4())

default_available_functions = {
    'current_date': datetime.datetime.now().date,
}

default_available_models = {
    'User': User
}

available_transformations = {
    'rotate': {'label': _(u'Rotate [degrees]'), 'arguments': [{'name': 'degrees'}]}
}

available_indexing_functions = {
    'proper_name': proper_name
}

register_settings(
    namespace=u'documents',
    module=u'documents.conf.settings',
    settings=[
        # Definition
        {'name': u'AVAILABLE_FUNCTIONS', 'global_name': u'DOCUMENTS_METADATA_AVAILABLE_FUNCTIONS', 'default': default_available_functions},
        {'name': u'AVAILABLE_MODELS', 'global_name': u'DOCUMENTS_METADATA_AVAILABLE_MODELS', 'default': default_available_models},
        {'name': u'AVAILABLE_INDEXING_FUNCTIONS', 'global_name': u'DOCUMENTS_INDEXING_AVAILABLE_FUNCTIONS', 'default': available_indexing_functions},
        # Upload
        {'name': u'USE_STAGING_DIRECTORY', 'global_name': u'DOCUMENTS_USE_STAGING_DIRECTORY', 'default': False},
        {'name': u'STAGING_DIRECTORY', 'global_name': u'DOCUMENTS_STAGING_DIRECTORY', 'default': u'/tmp/mayan/staging', 'exists': True},
        {'name': u'DELETE_STAGING_FILE_AFTER_UPLOAD', 'global_name': u'DOCUMENTS_DELETE_STAGING_FILE_AFTER_UPLOAD', 'default': False},
        {'name': u'STAGING_FILES_PREVIEW_SIZE', 'global_name': u'DOCUMENTS_STAGING_FILES_PREVIEW_SIZE', 'default': u'640x480'},
        {'name': u'ENABLE_SINGLE_DOCUMENT_UPLOAD', 'global_name': u'DOCUMENTS_ENABLE_SINGLE_DOCUMENT_UPLOAD', 'default': True},
        {'name': u'UNCOMPRESS_COMPRESSED_LOCAL_FILES', 'global_name': u'DOCUMENTS_UNCOMPRESS_COMPRESSED_LOCAL_FILES', 'default': True},
        {'name': u'UNCOMPRESS_COMPRESSED_STAGING_FILES', 'global_name': u'DOCUMENTS_UNCOMPRESS_COMPRESSED_STAGING_FILES', 'default': True},
        # Saving
        {'name': u'CHECKSUM_FUNCTION', 'global_name': u'DOCUMENTS_CHECKSUM_FUNCTION', 'default': default_checksum},
        {'name': u'UUID_FUNCTION', 'global_name': u'DOCUMENTS_UUID_FUNCTION', 'default': default_uuid},
        # Storage
        {'name': u'STORAGE_BACKEND', 'global_name': u'DOCUMENTS_STORAGE_BACKEND', 'default': FileBasedStorage},
        # Transformations
        {'name': u'AVAILABLE_TRANSFORMATIONS', 'global_name': u'DOCUMENTS_AVAILABLE_TRANSFORMATIONS', 'default': available_transformations},
        {'name': u'DEFAULT_TRANSFORMATIONS', 'global_name': u'DOCUMENTS_DEFAULT_TRANSFORMATIONS', 'default': []},
        # Usage
        {'name': u'PREVIEW_SIZE', 'global_name': u'DOCUMENTS_PREVIEW_SIZE', 'default': u'640x480'},
        {'name': u'PRINT_SIZE', 'global_name': u'DOCUMENTS_PRINT_SIZE', 'default': u'1400'},
        {'name': u'MULTIPAGE_PREVIEW_SIZE', 'global_name': u'DOCUMENTS_MULTIPAGE_PREVIEW_SIZE', 'default': u'160x120'},
        {'name': u'THUMBNAIL_SIZE', 'global_name': u'DOCUMENTS_THUMBNAIL_SIZE', 'default': u'50x50'},
        {'name': u'DISPLAY_SIZE', 'global_name': u'DOCUMENTS_DISPLAY_SIZE', 'default': u'1200'},
        {'name': u'RECENT_COUNT', 'global_name': u'DOCUMENTS_RECENT_COUNT', 'default': 40, 'description': _(u'Maximum number of recent (created, edited, viewed) documents to remember per user.')},
        {'name': u'ZOOM_PERCENT_STEP', 'global_name': u'DOCUMENTS_ZOOM_PERCENT_STEP', 'default': 50, 'description': _(u'Amount in percent zoom in or out a document page per user interaction.')},
        {'name': u'ZOOM_MAX_LEVEL', 'global_name': u'DOCUMENTS_ZOOM_MAX_LEVEL', 'default': 200, 'description': _(u'Maximum amount in percent (%) to allow user to zoom in a document page interactively.')},
        {'name': u'ZOOM_MIN_LEVEL', 'global_name': u'DOCUMENTS_ZOOM_MIN_LEVEL', 'default': 50, 'description': _(u'Minimum amount in percent (%) to allow user to zoom out a document page interactively.')},
        {'name': u'ROTATION_STEP', 'global_name': u'DOCUMENTS_ROTATION_STEP', 'default': 90, 'description': _(u'Amount in degrees to rotate a document page per user interaction.')},
        #Groups
        {'name': u'GROUP_SHOW_EMPTY', 'global_name': u'DOCUMENTS_GROUP_SHOW_EMPTY', 'default': True},
    ]
)
