from .models import UsageLog


class UsageLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user_agent = request.META['HTTP_USER_AGENT']

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        message = ''
        exclude_messages_status = [200, 500, 404, 401, 403]
        if response.status_code not in exclude_messages_status :
            message = str(response.content)
        data = {
            "method": request.method,
            "path": request.path,
            "ip": ip,
            "status_code": response.status_code,
            "response": message,
            "user_agent": user_agent,
        }

        log = UsageLog(**data)
        if request.user.id:
            log.user_id = request.user.id
        log.save()

        return response
