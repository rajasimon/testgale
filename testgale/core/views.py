import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Django channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from testgale.core.models import Crawler, Image


# Create your views here.
def index(request):
    return render(request, 'base.html')


@csrf_exempt
def crawl(request):
    json_body = json.loads(request.body)

    url = json_body['url']
    depth = json_body['depth']
    
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.send)(
        "crawler-process", 
        {
            "type": "generate", 
            "url": url,
            "depth": depth
        }
    )
    return JsonResponse({'status': True})


def result(request):
    url = request.GET.get('url')
    crawler = Crawler.objects.get(url=url)

    import pdb; pdb.set_trace()
    return JsonResponse({'status': True})