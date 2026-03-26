#metin temizleme kısmı
import logging
import re
import pandas

logger = logging.getLogger(__name__)

#tek bir metin üzerinden boşlukları temizle
def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


#DataFrame üzerinden tüm metin kolonlarını temizler
def clean_dataframe(dataframe: pandas.DataFrame) -> pandas.DataFrame:

    try:
        # 1. Boşluk temizleme
        dataframe = dataframe.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # 2. Eksik veri kontrolü
        missing_info = dataframe.isnull().sum()
        logger.info(f"Eksik veri durumu:\n{missing_info}")

        # 3. Tekrar eden satırları sil
        dataframe = dataframe.drop_duplicates()

        # 4. Tarih kolonlarını düzelt
        for column in dataframe.columns:
            if "date" in column.lower():
                dataframe[column] = pandas.to_datetime(dataframe[column], errors="coerce")

        # 5. Sayısal kolonları düzelt
        for column in dataframe.select_dtypes(include="object").columns:
            try:
                dataframe[column] = pandas.to_numeric(dataframe[column], errors="ignore")
            except Exception:
                pass

        logger.info("Temizleme işlemi tamamlandı.")
        return dataframe

    except Exception as error:
        logger.error(f"Temizleme hatası: {error}")
        return dataframe
