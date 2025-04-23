import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

ocr_model = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

def paddleocr_text(image: Image.Image) -> str:
    image_np = np.array(image)
    result = ocr_model.ocr(image_np, cls=True)
    return "\n".join([line[1][0] for line in result[0]])

def is_scanned_page(page) -> bool:
    return len(page.get_text().strip()) < 20
