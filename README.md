# TÜSEB Dental Anksiyete Projesi

Bu proje, "Giyilebilir IoT Sensör Sistemi ve Makine Öğrenmesi ile Hasta Anksiyetesi Ölçümü" projesinin yazılım bileşenlerini içermektedir. Projede donanım, yazılım ve veri analizi ekipleri paralel olarak çalışmaktadır.

Şu anki aşamada sadece **QR Kod ve MDAS Anket Modülü** tamamlanıp repoya eklenmiştir. Bu modül, hastaların anksiyete seviyelerini ölçmek için akıllı telefonları üzerinden anketi doldurmalarını sağlayan web formunu ve veritabanı altyapısını içerir.

## Mevcut Dosya Yapısı

* `mdas_projesi.py`: Web formunu ayağa kaldıran, QR kod üreten ve veritabanı bağlantılarını sağlayan ana uygulama dosyası.
* `templates/`: MDAS anketinin kullanıcı arayüzünü barındıran HTML dosyaları.
* `mdas_database.db_yeni`: Anket sonuçlarının kaydedildiği proje veritabanı dosyası.
* `.gitignore`: Çevre değişkenlerinin (`.env`) ve gereksiz önbellek dosyalarının GitHub'a yüklenmesini engelleyen ayar dosyası.

## Kurulum ve Çalıştırma

Projeyi lokal bilgisayarınızda çalıştırmak için ana dizindeyken terminalden ana Python dosyasını çalıştırmanız yeterlidir:

`python mdas_projesi.py`

*(Not: Uygulamanın API veya bulut kimlik doğrulama işlemleri için yerel dizininizde bir `.env` dosyası oluşturduğunuzdan emin olun.)*
