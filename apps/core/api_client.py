import logging
import requests

from requests.status_codes import codes

from apps.core.constants import (
    MAX_RETRY,
    TIMEOUT,
    DELETE,
    JSON_MIME_TYPE,
    HTTP_REQUEST_BODY_MIME_TYPE,
    CALLING_EXTERNAL_API,
    EXTERNAL_API_REQUEST_FAILED
)

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, max_retries=MAX_RETRY, timeout=TIMEOUT):
        self.max_retries = max_retries
        self.timeout = timeout

    def _get_request_kwargs(self, headers=None, params=None, data=None):
        request_headers = {
            "Accept": JSON_MIME_TYPE,
            "Content-Type": HTTP_REQUEST_BODY_MIME_TYPE,
        }

        if headers:
            request_headers.update(headers)

        request_kwargs = {
            "headers": request_headers,
            "timeout": self.timeout,
        }

        if params:
            request_kwargs["params"] = params

        if data:
            request_kwargs["json"] = data

        return request_kwargs

    def call_api(self, endpoint, method, data=None, params=None, headers=None):

        request_kwargs = self._get_request_kwargs(headers, params, data)

        request_method = getattr(requests, method)

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(
                    CALLING_EXTERNAL_API,
                    extra={
                        "endpoint": endpoint,
                        "method": method,
                        "attempt": attempt,
                    },
                )

                response = request_method(endpoint, **request_kwargs)
                response.raise_for_status()

                if (
                    response.status_code in {codes.ok, codes.created, codes.no_content}
                    and method != DELETE
                ):
                    return response.json()

            except requests.exceptions.RequestException:
                logger.exception(
                    EXTERNAL_API_REQUEST_FAILED,
                )

                if attempt == self.max_retries:
                    raise


api_client = APIClient()