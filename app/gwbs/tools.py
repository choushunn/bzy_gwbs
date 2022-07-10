from django.http import JsonResponse


def RJson(code, message, data):
    msg = {
        "code": code,
        "message": message,
        "result": [data]
    }
    return JsonResponse(msg, safe=False)
