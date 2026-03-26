#ocr modülleri,pdf,csv vb formatlar ile okuma işlemi
import os
import pandas 
import pytesseract
from PIL import Image
import pdfplumber
from src.database.db_connection import save_dataframe, save_and_return_id
from src.preprocessing.text_cleaner import clean_text

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#csv okuma 
def read_csv(file_path):
    return pandas.read_csv(file_path)

#pdf okuma
def read_pdf(file_path):
    text_data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text_data.append(page.extract_text())
    return "\n".join(text_data)

#resim dosyalarını okuma
def read_image(file_path, lang="eng"):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img, lang=lang)


def process_file(file_path, connection_string, user_id):
    ext = os.path.splitext(file_path)[1].lower()
    file_name = os.path.basename(file_path)

    # 1. Core tablosuna kayıt aç
    core_df = pandas.DataFrame([{
        "user_id": user_id,
        "file_name": file_name,
        "file_type": ext.replace(".", ""),
        "status": "processing"
    }])
    transaction_id = save_and_return_id(core_df, "transactions_core", connection_string, "transaction_id")

    # 2. İçeriği metadata’ya yaz
    if ext == ".csv":
        df = read_csv(file_path)
        meta_records = []
        for idx, row in df.iterrows():
            for col in df.columns:
                meta_records.append({
                    "transaction_id": transaction_id,
                    "meta_key": col,
                    "meta_value": str(row[col])
                })
        meta_df = pandas.DataFrame(meta_records)
        save_dataframe(meta_df, "transactions_metadata", connection_string)

    elif ext == ".pdf":
        text = read_pdf(file_path)
        cleaned = clean_text(text)
        meta_df = pandas.DataFrame([{
            "transaction_id": transaction_id,
            "meta_key": "content",
            "meta_value": cleaned
        }])
        save_dataframe(meta_df, "transactions_metadata", connection_string)

    elif ext in [".png", ".jpg", ".jpeg"]:
        text = read_image(file_path)
        cleaned = clean_text(text)
        meta_df = pandas.DataFrame([{
            "transaction_id": transaction_id,
            "meta_key": "content",
            "meta_value": cleaned
        }])
        save_dataframe(meta_df, "transactions_metadata", connection_string)

    else:
        print("Desteklenmeyen format:", ext)
