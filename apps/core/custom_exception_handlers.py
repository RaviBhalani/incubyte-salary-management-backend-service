from rest_framework.serializers import ValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, Throttled, NotAuthenticated, AuthenticationFailed, PermissionDenied, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import set_rollback
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
    HTTP_405_METHOD_NOT_ALLOWED
)
from apps.core.constants import (
    THROTTLE_EXEC_DETAILS,
    NOT_FOUND_EXEC_DETAILS,
    VALIDATION_EXEC_DETAILS,
    INTERNAL_ERROR_EXEC_DETAILS,
    API_EXC_DEFAULT_CODE,
    PERMISSION_DENIED_EXEC_DETAILS,
    NOT_AUTHENTICATED_EXEC_DETAILS,
    AUTHENTICATION_FAILED_EXEC_DETAILS,
    METHOD_NOT_ALLOWED_EXEC_DETAILS
)


def get_response(
        data=None,
        message: str = None,
        error_list: list = None,
        headers: dict = None,
        success: bool = False,
        no_content: bool = False,
        resource_created: bool = False,
        permission_denied: bool = False,
        missing_resource: bool = False,
        bad_request: bool = False,
        server_error: bool = False,
        unauthorized: bool = False,
        method_not_allowed: bool = False

):
    status_code: status = None
    if not error_list:
        error_list = list()
    if no_content:
        status_code = HTTP_204_NO_CONTENT
    elif success:
        status_code = HTTP_200_OK
    elif resource_created:
        status_code = HTTP_201_CREATED
    elif permission_denied:
        status_code = HTTP_403_FORBIDDEN
    elif missing_resource:
        status_code = HTTP_404_NOT_FOUND
    elif bad_request:
        status_code = HTTP_400_BAD_REQUEST
    elif server_error:
        status_code = HTTP_500_INTERNAL_SERVER_ERROR
    elif unauthorized:
        status_code = HTTP_401_UNAUTHORIZED
    elif method_not_allowed:
        status_code = HTTP_405_METHOD_NOT_ALLOWED

    response_data = {
        'data': data,
        'message': message,
        'error_list': error_list,
        }

    return Response(status=status_code, headers=headers, data=response_data)


class APIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = VALIDATION_EXEC_DETAILS
    default_code = API_EXC_DEFAULT_CODE

    def __init__(self, detail=None, code=None, status_code=status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        super().__init__(detail, code)


def custom_exception_handler(exc, context):
    print("➡ exc :", exc)
    print("➡ context :", context)

    not_found: bool = False
    server_error: bool = False
    bad_request: bool = False
    unauthorized: bool = False
    permission_denied: bool = False
    method_not_allowed: bool = False

    if isinstance(exc, Throttled):
        exc.detail = THROTTLE_EXEC_DETAILS % exc.wait

    
    elif isinstance(exc, NotAuthenticated):
        if not hasattr(exc, 'default_detail'):
            exc.default_detail = NOT_AUTHENTICATED_EXEC_DETAILS
        unauthorized = True

    elif isinstance(exc, AuthenticationFailed):
        if not hasattr(exc, 'default_detail'):
            exc.default_detail = AUTHENTICATION_FAILED_EXEC_DETAILS
        unauthorized = True

    elif isinstance(exc, MethodNotAllowed):
        if not hasattr(exc, 'default_detail'):
            exc.default_detail = METHOD_NOT_ALLOWED_EXEC_DETAILS
        method_not_allowed = True   

    elif isinstance(exc, APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait
        set_rollback()

    elif isinstance(exc, Http404):
        if not hasattr(exc, 'default_detail'):
            exc.default_detail = NOT_FOUND_EXEC_DETAILS
        not_found = True

    elif isinstance(exc, ValidationError):
        if not hasattr(exc, 'default_detail'):
            exc.default_detail = VALIDATION_EXEC_DETAILS
        bad_request = True

    elif isinstance(exc, PermissionDenied):
        if not hasattr(exc, 'default_detail'):
            exc.default_detail = PERMISSION_DENIED_EXEC_DETAILS       
        permission_denied = True

    elif isinstance(exc, Exception):
        if not hasattr(exc, 'default_detail'):
            exc.default_detail = INTERNAL_ERROR_EXEC_DETAILS
        if not hasattr(exc, "status_code"):
            server_error = True
    else:
        server_error = True

    error_list = []
    try:
        error_details = exc.get_full_details()
        if isinstance(error_details, dict):
            if "message" in error_details:
                error_list.append(error_details["message"])
            else:
                for key, value in error_details.items():
                    if isinstance(value, dict):
                        error_list.append(f"{key}: {value['message']}")
                    elif isinstance(value, list):
                        for error_message in value:
                            error_list.append(f"{key}: {error_message['message']}")
                    elif isinstance(value, str):
                        error_list.append(f"{key}: {value}")
        else:
            for error_item in error_details:
                error_list.append(error_item["message"])

    except Exception:
        error_list.append(str(exc))

    return get_response(
        error_list=error_list,
        missing_resource=not_found,
        server_error=server_error,
        bad_request=bad_request,
        unauthorized=unauthorized,
        permission_denied=permission_denied,
        method_not_allowed=method_not_allowed
    )