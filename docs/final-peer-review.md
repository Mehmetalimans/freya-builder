# Final öncesi Miraç değişiklikleri

İncelenen kayıtlar: 93ee9d4 ve 1bb2d4c; değişiklikler korunmuştur. Final dalı, daha önce incelenip birleştirilmiş 1b2ac29 tabanından ayrıldı. PR #7 bu tabandaki `fix/mirac-integration-review` dalına yöneliktir; main veya Miraç dalı değiştirilmedi.

- Klasör okuyucu yalnız üst dizindeki Markdown/TXT dosyalarını okuyor. Finalin e-posta ekleri, toplantı dökümü ve iç içe servis belgeleri kaçırılıyor. Yeni klasör adaptörü tüm belgeleri envanterler ve üretim sırasında okutur.
- OpenAPI bulunamazsa practice OpenAPI dosyasına geri dönülüyor. Bu, final mock adresinde eski tahsilat uç noktalarını üretir; final için geçerli bir sözleşme değildir. Yeni adaptör gerçek belge eksikse üretimi engeller.
- `.workers.dev` alanına izin verilmesi URL uyumluluğudur; yeni yedi servis sözleşmesini veya Türkçe kuralları oluşturmaz. Final kendi doğrulanmış mock origin'iyle sınırlıdır.
- Yeni test practice klasörünü ve eski yedi aracı doğruluyor; gerçek final desteğinin kanıtı değildir. Canlı doğrulama testi anahtar yoksa API çağrısı yapmadan geçebiliyor; bunu canlı doğrulama başarısı olarak sunmuyoruz.

Bu değişiklikler final yoluna kopyalanmadı. Eski practice ölçümleri tarihsel olarak korunuyor. Final canlı başarısı ayrı workflow sürümü, çağrı kaydı ve süre/maliyet farkıyla ölçülecek.
