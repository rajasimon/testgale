import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Django channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from testgale.core.models import Crawler, Image
from testgale.core.serializers import CrawlerSerializer


# Create your views here.
def index(request):
    """
    Show React page on the frontend.
    """
    return render(request, 'base.html')


@csrf_exempt
def crawl(request):
    # Get json from the body request
    json_body = json.loads(request.body)

    # Get url and depth from json
    url = json_body['url']
    depth = json_body['depth']

    # First try to get the crawler objecgt from database if one exists
    crawler = Crawler.objects.filter(url=url).first()

    """
    Two things, One is we need to tell the frontend to showcase the results
    if existing results found in database. And another one this is to tell
    the backend to run the crawler process if none exists as well as show
    the frontend loader screen.
    """
    if crawler:
        return JsonResponse({'status': True})
    else:
        # No crawler found in this case we need to start the crawler process
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.send)(
            "crawler-process", 
            {
                "type": "generate", 
                "url": url,
                "depth": depth
            }
        )

        # Return False so that frontend will load the spinner.
        return JsonResponse({'status': False})


def result(request):
    """
    To fetch the images from the database.
    """
    # Note: It should accept POST method.
    url = request.GET.get('url')

    # Ask restframework to serialize the datas
    crawler = Crawler.objects.get(url=url)
    serializer = CrawlerSerializer(crawler)
    return JsonResponse(serializer.data, status=200)
