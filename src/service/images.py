import shutil

from fastapi import UploadFile, BackgroundTasks

from src.service.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):
    def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as f:
            shutil.copyfileobj(file.file, f)
        resize_image.delay(image_path)
        # background_tasks.add_task(resize_image, image_path) # Не круто - медленно!
