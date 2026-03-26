#file_reader ve text_cleaner modüllerini kullanarak dosya okuma ve temizleme işlemlerini yapar.
#db_connection modülünü kullanarak temizlenen veriyi veri tabanına kaydeder.
from src.reader.file_reader import process_file
from src.preprocessing.text_cleaner import clean_dataframe
from src.database.db_connection import save_dataframe
from fastapi import FastAPI
from backend.src.api import app

connection_string = "mysql+pymysql://root:1234@localhost:3306/fintech_db"
app = FastAPI()
app.include_router(app,prefix="/api/auth")
if __name__ == "__main__":
    #frontent ile baglandıgında otomatik gerçeklesecek
    file_path = "data/sample_finance.csv"
    user_id = 1  # test için users_core tablosunda bir kullanıcı ekle

    # 1. Dosyayı oku → DataFrame
    dataframe = process_file(file_path, connection_string, user_id)

    # 2. DataFrame’i temizle
    cleaned_dataframe = clean_dataframe(dataframe)

    # 3. Temizlenmiş DataFrame’i MySQL’e kaydet
    save_dataframe(cleaned_dataframe, "transactions_core", connection_string)
