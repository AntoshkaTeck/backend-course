import os.path

from PIL import Image, ImageOps
from time import sleep

from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    sleep(5)
    print("Test task")


@celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    img = Image.open(image_path)
    # 💡 Исправляем ориентацию по EXIF
    img = ImageOps.exif_transpose(img)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        new_file_name = f"{name}_{size}px_{ext}"
        output_path = os.path.join(output_folder, new_file_name)
        img_resized.save(output_path)

    print(f"Resized image to {output_folder}")