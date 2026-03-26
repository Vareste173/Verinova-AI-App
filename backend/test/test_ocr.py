#ocr sistemini test etmek için kullanılan test dosyası
import pytesseract
from PIL import Image

if __name__ == "__main__":
    image_path = "data/sample_image.png"
    text = pytesseract.image_to_string(Image.open(image_path))
    print("OCR çıktısı:", text)
