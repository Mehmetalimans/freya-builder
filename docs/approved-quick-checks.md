# 11 Ekim onaylı uygulama

Kullanıcı 30 dakikalık düzeltme kapsamını onayladı, ardından yeni görev öncesi
son test aşamasını beş dakikayla sınırladı. Önceki 100 USD ve 20 USD tampon
sınırlarını kaldırdı. Yalnız mevcut Freya deneme kredisi kullanılacak.

## Tamamlanan değişiklikler

- Miraç'ın integration/v3-final dalındaki 3d731be kaydı birleştirildi; önceki
  yerel değerlendirme ve kurtarma değişiklikleri korunmuş commit'lere alındı.
- Başarılı kimlik cevaplarını yerelde sayıp all_verified üretmek kaldırıldı.
  OpenAPI'de boolean olarak bildirilen all_verified veya identity_complete
  gerekir; tamamlanma alanı yoksa üretim durur.
- Transfer kuyruğu ile kapanış nedeni ayrıldı. Kaynak brief'in kayıt bildirimi,
  ikna sınırları, takvim ve belirsiz tarih korumaları korundu.
- C/D/E örnekleri uygun sentetik şema ile derleniyor; canlı başarı iddiası yok.
- Mevcut kredi izni bütçe kontrolüne eklendi; negatif/sıfır kredi, eşzamanlı
  simülasyon ve yetkisiz harcama kontrolleri devam ediyor.
- Paket kontrolünün yakaladığı eksik briefs/ klasörü release allowlist'ine
  eklendi. İlk temiz ortam denemesi bu nedenle başarısızdı; sonraki deneme geçti.

## Kanıt ve sınırlar

Sürüm 0.1.15: 114 test temiz, üçüncü taraf bağımlılıksız Python 3.12.14
ortamında geçti. A hash b901ea4cf296055065873a35e81512202cf3703392f8250e954d30cfcbeb0703;
B hash fbaef380f02faf4f11cef4a2ea69f64c43d6b51bb3b7923628f47f8224578193.
Her ikisi iki üretimde eşitti. Bu kanıt canlı benchmark puanı değildir.

Eski eksik B koşusunun ilk uzak simülasyonu artık HTTP 404 döndürüyor.
Diğer simülasyondaki bütün çağrılar bitmiş ve workspace'te aktif simülasyon
yoktu. Rezerv bu kanıtla uzlaştırıldı, eksik B ölçümü başarıya çevrilmedi.
Eski kayıt ve rezerv yedeği yerelde korundu.

Hızlı canlı ölçüm: A PUB-03 ve PUB-07 birer tekrar **2/2 geçti**, 91,625 saniye,
başarısız araç sonucu 0. Gözlenen bakiye farkı 0,09145 USD; gerçek fatura
bilinmiyor. Practice-a workflow'u v14 olarak yayın/export/geri okundu.
Transfer ve servis hatası için PUB-09/PUB-10 ikinci ölçümü **2/2 geçti**,
67,891 saniye, gözlenen bakiye farkı 0,07 USD. Servis hatası vakasında beklenen
ilk create_promise hatasından sonra tekrar başarılı oldu. Toplam dört public
vaka birer kez geçti, gözlenen bakiye farkı 0,16145 USD. İki simülasyon da
completed; test sonrası kaynak/export sürüm kontrolü hâlâ v14. Yeni test veya
workflow değişikliği başlatılmadı. Sonuç reports/approved-quick-evaluation.json.

Son fetch sırasında Miraç'ın yeni 3ffd864 kaydı görüldü. Kullanıcı çakışmayı
önlemek için uyardı; yeni kaynak/workflow değişikliği durduruldu. Bu kayıt
henüz birleştirilmedi: sahte kimlik sayacı, reason=queue ve sabit politika
talimatlarının önceki dalda kalmasına karşı ayrıca karşılaştırılmalı. Commit
başlığındaki yüzde 100 başarı, bizim sürümün ölçümü olarak kabul edilmedi.

Önceki 0.1.13 başarıları bu sürümün skoru değildir. Duygu etiketi yoksa
memnuniyet oranı bilinmiyor. Public vakalar regresyondur; bağımsız genelleme
ve gizli final başarısı henüz ölçülmedi. Teslim yapılmadı; main birleştirmesi
ekip incelemesine bağlıdır.
