from .models import IPAddress
class SaveIPMiddleware:
    def __init__(self , get_response):
        self.get_response = get_response
    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')


        try:
            ip_address = IPAddress.objects.get(ipAddr=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress(ipAddr=ip)
            ip_address.save()
        request.user.ip_address = ip_address
        response = self.get_response(request)

        return response