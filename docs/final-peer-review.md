# Final öncesi Miraç değişiklikleri

İncelenen kayıtlar: 93ee9d4 ve 1bb2d4c; değişiklikler korunmuştur. Final dalı, daha önce incelenip birleştirilmiş 1b2ac29 tabanından ayrıldı. PR #7 mevcut `integration/v3-final` dalına yöneliktir. Tabanı önceki inceleme dalına çevirme isteği otomatik güvenlik incelemesince reddedildi; hedef değişmedi. Main veya Miraç dalı değiştirilmedi. PR olası birleştirme çatışmaları ayrıca inceleme gerektirir; teslim kaynağı ayrı final dalındaki kesin commit olacaktır.

- Klasör okuyucu yalnız üst dizindeki Markdown/TXT dosyalarını okuyor. Finalin e-posta ekleri, toplantı dökümü ve iç içe servis belgeleri kaçırılıyor. Yeni klasör adaptörü tüm belgeleri envanterler ve üretim sırasında okutur.
- OpenAPI bulunamazsa practice OpenAPI dosyasına geri dönülüyor. Bu, final mock adresinde eski tahsilat uç noktalarını üretir; final için geçerli bir sözleşme değildir. Yeni adaptör gerçek belge eksikse üretimi engeller.
- `.workers.dev` alanına izin verilmesi URL uyumluluğudur; yeni yedi servis sözleşmesini veya Türkçe kuralları oluşturmaz. Final kendi doğrulanmış mock origin'iyle sınırlıdır.
- Yeni test practice klasörünü ve eski yedi aracı doğruluyor; gerçek final desteğinin kanıtı değildir. Canlı doğrulama testi anahtar yoksa API çağrısı yapmadan geçebiliyor; bunu canlı doğrulama başarısı olarak sunmuyoruz.

Bu değişiklikler final yoluna kopyalanmadı. Eski practice ölçümleri tarihsel olarak korunuyor. Final canlı başarısı ayrı workflow sürümü, çağrı kaydı ve süre/maliyet farkıyla ölçülecek.
