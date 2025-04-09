import os
import subprocess
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video

@receiver(post_save, sender=Video)
def convert_to_hls(sender, instance, created, **kwargs):
    if created:  # Только при создании нового видео
        input_path = instance.file.path  # Путь к загруженному файлу
        output_dir = os.path.join(os.path.dirname(input_path), "hls", str(instance.id))
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "index.m3u8")

        # Запускаем ffmpeg для конвертации
        command = [
            "ffmpeg", "-i", input_path,
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            "-start_number", "0",
            "-hls_time", "10",
            "-hls_list_size", "0",
            "-f", "hls", output_path
        ]
        
        subprocess.run(command, check=True)
        print(f"✅ Видео {instance.file.name} успешно конвертировано в HLS")
