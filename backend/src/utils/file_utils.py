#yardımcı araçlar
import os
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
def get_logger(file_name:str):
    return logging.getLogger(file_name)
    
#dosya yolunu isim ve uzantısına ayırır ve küçük harfe çevirir bu sayade dosya yoluna göre işlem yapılır.
def get_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1].lower()

#dosyanın tam yolundan dosya adını çıkarır.
def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)

#dosyanın gerçekten var olup olmadıgını kontrol eder.
def validate_file(file_path: str, allowed_extensions=None) -> bool:
    if not os.path.exists(file_path):
        return False
    if allowed_extensions:
        ext = get_extension(file_path)
        return ext in allowed_extensions
    return True

#dosya boyutunu byte cinsinden hesaplar
def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)
