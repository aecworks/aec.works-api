from django.middleware.csrf import CsrfViewMiddleware, get_token


class EnsureCsrfCookie(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        retval = super(EnsureCsrfCookie, self).process_view(
            request, callback, callback_args, callback_kwargs
        )
        # Forces process_response to send the cookie
        get_token(request)
        return retval
