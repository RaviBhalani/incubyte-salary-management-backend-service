"""
Environments start.
"""

LOCAL = 'local'
DEV = 'dev'
TEST = 'test'
PROD = 'prod'

"""
Environments end.
"""


"""
Constants for custom_exception_handler start
"""

THROTTLE_EXEC_DETAILS = "request limit exceeded available in %d seconds"
NOT_FOUND_EXEC_DETAILS = "Item Not Found"
VALIDATION_EXEC_DETAILS = "Validation Error"
INTERNAL_ERROR_EXEC_DETAILS = "Internal Server Error"
PERMISSION_DENIED_EXEC_DETAILS = "You are not authorised to perform this action"
NOT_AUTHENTICATED_EXEC_DETAILS = "Authentication credentials were not provided"
AUTHENTICATION_FAILED_EXEC_DETAILS ="Authentication failed"
METHOD_NOT_ALLOWED_EXEC_DETAILS = "Method Not Allowed"

API_EXC_DEFAULT_CODE = "error"

"""
Constants for custom_exception_handler ends
"""


"""
Constants for logger_mixin start
"""

ANONYMOUS = "Anonymous"

"""
Constants for logger_mixin ends
"""


"""
Constants for APP Names starts
"""

CORE_APP = "apps.core"

"""
Constants for APP Names ends
"""


"""
API methods start.
"""

CREATE = 'create'
RETRIEVE = 'retrieve'
LIST = 'list'
UPDATE = 'update'
PARTIAL_UPDATE = 'partial_update'
DESTROY = 'destroy' 

"""
API methods end.
"""


"""
Constants for pagination settings starts
"""

PAGE_SIZE = 25
MAX_PAGE_SIZE = 200

"""
Constants for pagination settings ends
"""


"""
Constants for Teams integration starts
"""

TEAMS_MESSAGE_TYPE = "message"
TEAMS_CONTENT_TYPE = "application/vnd.microsoft.card.adaptive"
TEAMS_CARD_TYPE = "AdaptiveCard"
TEAMS_BLOCK_TYPE = "TextBlock"
TEAMS_SCHEMA = "http://adaptivecards.io/schemas/adaptive-card.json"
TEAMS_CARD_VERSION = "1.0"

"""
Constants for Teams integration ends
"""


"""
Constants for API client starts
"""

CALLING_EXTERNAL_API = "Calling external API"
EXTERNAL_API_REQUEST_FAILED = "External API request failed"

MAX_RETRY = 3
TIMEOUT = 10

REQUEST_FAILED = "External API request failed"

JSON_MIME_TYPE = "application/json"
HTTP_REQUEST_BODY_MIME_TYPE = "application/x-www-form-urlencoded"

"""
Constants for API client ends
"""


"""
HTTP methods start.
"""

GET = 'get'
POST = 'post'
PUT = 'put'
PATCH = 'patch'
DELETE = 'delete'

"""
HTTP methods end.
"""
