from fastapi import UploadFile, APIRouter
import shutil

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix='/images',
    tags=['Загрузка картинок']
)

@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile):
    path_img = f'app/static/images/{name}.webp'
    with open(path_img, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(path_img)

