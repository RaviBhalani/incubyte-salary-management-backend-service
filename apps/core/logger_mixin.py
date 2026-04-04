import logging
from .constants import ANONYMOUS

class LoggingMixin:
    """
    Provides full logging of requests and responses.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('django.request')

    def initial(self, request, *args, **kwargs):
        try:
            self.logger.info({
                "request": request.data,
                "args": args,
                "kwargs": kwargs,
                "method": request.method,
                "endpoint": request.path,
                "user": request.user.id if request.user.is_authenticated else ANONYMOUS
            })
        except Exception:
            self.logger.exception("Error logging request data")
        super().initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        try:
            self.logger.info({
                "response": response.data,
                "args": args,
                "kwargs": kwargs,
                "status_code": response.status_code,
                "user": request.user.id if request.user.is_authenticated else ANONYMOUS
            })
        except Exception:
            self.logger.exception("Error logging response data")
        return super().finalize_response(request, response, *args, **kwargs)