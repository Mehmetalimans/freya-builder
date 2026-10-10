# Son kontroller — 11 Ekim 2026

Kullanıcı son testleri sürdürmeye ve müşteri iletişimini iyileştirmeye izin verdi.
Ara verme talimatı bu çalışma için kaldırıldı; ortak 100 USD Freya sınırı ve
tek eşzamanlı simülasyon geçerli. Dış model API harcaması yok.

## İnceleme ve birleşim

Miraç'ın `1aefb49`, `803203f`, `5494a2e` değişiklikleri aynı PR dalında
birleştirildi. Ek davranış alanlarını geri okuma kontrolü, yayın sürümü
bağlama fikri, ürün listesini okuyabilme, açık iş haftası ve doğal tarih
biçimleri korundu. Yayın kontrolündeki tüm export hash'i karşılaştırması
düzeltildi: Freya'nın eklediği agent yapılandırması yerel taslağın hash'ini
değiştirir; yerel kaynak hash'i ve davranış alanlarının geri okuması ayrı
kontrol edilir. Yayınlanmamış sürüm başarı sayılmaz.

Yeni `parse_policy`/hook talimatları çıkarıldı: varsayılan üç kimlik denemesi,
takvim bantları, sabit SMS/tekrar kuralları ve enum listesinin ilk/son elemanını
iş anlamı gibi seçmek görülmemiş brief'lerde güvenilir değildir. Doğrulanmış
v3 banka hostu korunur; yeni host desteklenmiş sayılmaz. İş haftası açık
tanımlanmamışsa tatil örneklerinden takvim varsayılmaz. Gün sayısı sınırında
`after today/call date/now` ankrajı gerekir. Eksik gecikme değeri sıfır yapılmaz.
Önceki null ve boolean regresyon testleri korunur.

`5494a2e` kaynağı ayrı yerel arşivde aynı 13 regresyon testiyle denetlendi:
alt senaryolar dahil 16 başarısız assertion ve 3 hata; birleşik aday aynı
13 testi geçti. Kanıt `reports/mirac-review-regressions.json` içine eklendi.

Teslim paketleyicisi temiz Git kaydı ister; bilinmeyen commit kabul etmez.
Çevrimdışı deneme final slotlarını yayımlayamaz ve her paket ayrı klasöre
yazılır. Public deneme final teslimi sayılmaz.

## Müşteri iletişimi ve duygu verisi

0.1.13 genel talimatı kısa ve nazik yanıt, müşterinin belirttiği sorunu kısaca
tanıma, soruyu cevaplama, izin verilen alternatifleri açıklama ve baskısız
kapanış ekler. Zorunlu açılış, onay, politika, deneme sayısı ve banka kayıtları
korunur. Müşterinin hisleri veya başarı sonucu uydurulmaz.

Freya UI'daki **Duygu yok** analizi olmayan çağrıları gösterir. Önceki 21
çağrının analysis alanında yalnız successEvaluation vardı. Minimal belgeli
analytics sorgusu 1 very-unhappy, 1 unhappy ve 0 happy/very-happy döndürdü;
UI'nın 10 Ekim aralığı 86 çağrı içeriyor. Kapsam ve asistan filtresi eşleşmediği
için bunlardan bu builder'a ait bir memnuniyet yüzdesi hesaplanmaz.
Yeni ölçümlerde duygu alanı yoksa oran `null` kalır. Mevcut başarı scorer'ı
değiştirilmez, duygu etiketleri elle yazılmaz ve analiz sonucuna olumlu puan
vermeyi isteyen talimat eklenmez.

## Önceki ölçümün kurtarılması

0.1.11'in üçüncü turu duraklatılan worker'dan sonra uzakta tamamlandı. Bütün
21 mevcut çağrı resmî scorer ve mevcut banka oturumlarıyla salt okunur
kurtarıldı: 6/7, 7/7, 7/7; üç tekrarda da geçen **6/7**, toplam **20/21**.
Tam tur süresi ölçülmedi; kurtarma süresi yeni simülasyon süresi değildir.
Orijinal ara kaydı korundu, bekleyen bütçe rezervi tüketim sorgusuyla kapatıldı.

## Son aday ölçümü

0.1.13: 102 yerel test geçti; canlı ölçüm henüz tamamlanmadı. A geliştirme
7 vaka × 3, kalan A 3 × 3 ve B 3 × 3 aynı sabit adayla ölçülecek. B public
vakaları ekipçe kullanılmıştır; regresyondur. Gizli final brief'leri ve final
teslimi bu public ölçümden ayrıdır.

0.1.13 A ölçümü tamamlandı: geliştirme 7/7 (21/21 çağrı), kalan A 2/3
(7/9 çağrı). PUB-10 ilk iki tekrarda değerlendirici, zorunlu çağrı kayıt
bildirimindeki "recorded" sözcüğünü ödeme işleminin başarı iddiası olarak
yorumladı; aynı vakada banka ledger'ı doğruydu, son tekrar geçti. Bu bir
değerlendirici yorumu belirsizliğidir; skor değiştirilmedi. Son A turunun
durum alanı bir süre running kaldı; bütün çağrıların/verdict'lerin sona
erdiği doğrulanarak pause istendi. Platform bu sırada doğal completed
durumuna geçti, orijinal resmî ölçüm oluştu. Gereksiz kurtarma denemesi
yeni çağrı başlatmadan durduruldu; ölçülmüş koşuyu yeniden kurtarma
engeli ve regresyon testi eklendi.

0.1.14 adayı, anlamıyla tarif edilmiş kayıt bildirimini "we are recording
this call" biçiminde ifade ederek banka işlemi başarısından açıkça ayırır.
Brief exact/verbatim bir metin verirse o metin korunur. Vaka kimliği,
müşteri tarihi veya scorer cevabı üreticiye gömülmedi. 105 yerel test geçti.
Bu düzeltmede kalan A artık geri bildirim için görüldüğü için sonraki
tekrarları bağımsız genelleme değil regresyon ölçümüdür.

Son aday için bir sınırlı 39-çağrılık tur daha ayrıldı: tarihsel kota
32 simülasyon/156 vaka koşusu (planlanan sayaç 147). 100 USD izin ve
20 USD tampon aynı. Yerel eşzamanlı çağrı tavanı tek simülasyon içinde
3'e çıktı; resmî kit varsayılanı 5 ve belgeli maxConcurrentCalls özelliği
kullanılır. 0.1.13 iki çağrıyla, 0.1.14 üç çağrıyla ölçülür; bu değişiklik
yüzünden süre farkı yalnız prompt düzenlemesine atfedilemez.
