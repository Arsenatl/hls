from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from django.conf import settings
import subprocess
import os

from .models import Video
from .serializer import VideoSerializer

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_video(request):
    """ Загружаем видео и конвертируем его в HLS """
    video = request.FILES['video_file']
    instance = Video.objects.create(video_file=video, title=request.data.get('title', ''))
    instance.save()

    # Конвертация в HLS с помощью ffmpeg
    video_path = instance.video_file.path
    hls_path = os.path.join(settings.MEDIA_ROOT, "hls", str(instance.id))
    os.makedirs(hls_path, exist_ok=True)

    hls_file = os.path.join(hls_path, "index.m3u8")

    ffmpeg_cmd = [
        "ffmpeg", "-i", video_path, "-c:v", "libx264", "-b:v", "1000k",
        "-hls_time", "10", "-hls_list_size", "0", "-f", "hls", hls_file
    ]
    subprocess.run(ffmpeg_cmd)

    return Response({"message": "Видео загружено", "hls_url": f"/media/hls/{instance.id}/index.m3u8"})

@api_view(['GET'])
def list_videos(request):
    """ Получаем список видео """
    videos = Video.objects.all()
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)
