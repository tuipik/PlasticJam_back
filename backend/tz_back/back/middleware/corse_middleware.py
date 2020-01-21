from django.conf import settings


class CorsMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        cores_header_value = f'http://{settings.SITE_IP}'
        if request.path_info == '/api/users/':
            cores_header_value = 'http://plasticjam.com/'
        response['Access-Control-Allow-Origin'] = cores_header_value
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
