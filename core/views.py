from django.http import JsonResponse
from django.views.generic.base import View
import logging


JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}
logger = logging.getLogger(__name__)


class BaseView(View):
    """
    Base class for all views, handles exceptions.
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.warning(e)
            return self._response({'errorMessage': str(e)}, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params=JSON_DUMPS_PARAMS
        )
