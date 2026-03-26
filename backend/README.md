# Verinova_app AI için Veri İşleme 

Bu kısımda, farklı formatlardaki dosyaları (CSV, PDF, görsel) okuyup temizleyerek MySQL veritabanına aktaran modüler bir veri işleme sistemi oluşturulmuştur.  
Amaç: Kullanıcıların yüklediği finansal verileri otomatik olarak işlemek ve güvenilir şekilde veritabanına kaydetmektir.

---

##  Proje Yapısı

📂 src/  
 ├── reader/  
 │   └── file_reader.py   # Dosyaokuma ve DataFrame oluşturma  
 ├── preprocessing/  
 │   └── text_cleaner.py  # Veri temizleme (boşluk, eksik veri, tekrar, format düzeltme)  
 ├── database/  
 │   └── db_connection.py # MySQL bağlantısı ve veri kaydetme  
 └── main.py              # İş akışını başlatan kontrol dosyası  

📂 data/ 
 ├── raw/        # Test aşamasında kullanılan, orijinal dosyalar  
 ├── processed/  # Test aşamasında kullanılan, temizlenmiş dosyalar  

> Not: Proje canlıya geçtiğinde kullanıcı dosyaları frontend üzerinden yüklenip doğrudan işlenecektir. Bu klasörler sadece geliştirme sürecinde var olacaktır..

---

## 🔄 Veri İşleme Süreci

1. **file_reader** → Dosya okunur, DataFrame oluşturulur.  
2. **text_cleaner** → DataFrame temizlenir (eksik veri, tekrar, format düzeltme).  
3. **db_connection** → Temizlenmiş DataFrame MySQL veritabanına kaydedilir.  

---

