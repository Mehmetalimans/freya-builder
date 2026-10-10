# Miraç entegrasyon incelemesi ve düzeltmeler — 10 Ekim 2026

İncelenen son dal `integration/v3-final`, commit
`7dc5e56f6e4d83f0ad03a395120e9a2bbcbafc41`. Önceki `feat/agent-core-optimization`
dalındaki `4a29e54` düzeltmeleri ve sonraki entegrasyon değişiklikleri birlikte
incelendi. Düzeltme dalı bu son entegrasyon commit'inden açıldı; iki kişinin
geçmişi korundu, ana dala veya Miraç'ın dalına doğrudan değişiklik gönderilmedi.

## Bulgular ve uygulanan düzeltmeler

| Öncelik | Hata ve etkisi | Düzeltme / doğrulama |
| --- | --- | --- |
| P1 | [Takvim talimatı](https://github.com/Mehmetalimans/freya-builder/blob/7dc5e56f6e4d83f0ad03a395120e9a2bbcbafc41/builder/core.py#L237) hâlâ 14 Ekim 2026'yı bugün ve 26 Ekim'i zorunlu tatil sayıyordu. Farklı brief/`now` ile kodun hesapladığı takvimle çelişiyordu. | Sabit örnekler kaldırıldı; yalnız tanınan brief takvimi ve çağrıdaki `now` kullanılır. Tanınmayan takvimde hafta günleri/tatiller tahmin edilmez. 2031 tarihli sentetik girdide eski tarihler üretilmiyor. |
| P1 | [Kimlik talimatı ve hata protokolü](https://github.com/Mehmetalimans/freya-builder/blob/7dc5e56f6e4d83f0ad03a395120e9a2bbcbafc41/builder/core.py#L287) servis hatasını yanlış cevap sayıyordu; hook düzelse bile prompt çelişkisi kalmıştı. | Taşıma/`ok=false` hatası ile `verified=false` ayrıldı. Hook doğrulanmamış yanıt için soru, üç deneme veya kapanış nedeni uydurmuyor. |
| P1 | [Hook'lar](https://github.com/Mehmetalimans/freya-builder/blob/7dc5e56f6e4d83f0ad03a395120e9a2bbcbafc41/builder/core.py#L122) başarısız `get_account` yanıtını "Account loaded" diye sunabiliyordu. Ayrıca `"false"` metni Python'da doğru kabul edilip başarılı kayıt/doğrulama gibi yorumlanıyordu. | Başarı için gerçek boolean `True` aranır; hata zarfından başarı talimatı çıkmaz. Ham banka alanları değiştirilmez; yalnız doğrulanmış durumu açıklayan ek metin yazılır. |
| P1 | [Sabit politika](https://github.com/Mehmetalimans/freya-builder/blob/7dc5e56f6e4d83f0ad03a395120e9a2bbcbafc41/builder/core.py#L355) soru sırası, deneme limiti, callback saatleri, bantlar, SMS ve kapanış enum'larını brief'ten bağımsız dayatıyordu. Hook her başarısız söz için yeniden bir tekrar emri veriyordu. | Tam brief korunarak sabit iş kararları kaldırıldı. Hook'lar yeni retry bütçesi veya kapanış enum'u üretmez; önceki denemeleri ve diğer ürünleri dikkate alarak verilen politikayı izlemeyi söyler. Değişen enum/SMS/kimlik politikalarıyla sentetik regresyonlar eklendi. |
| P2 | [Null şema işleme](https://github.com/Mehmetalimans/freya-builder/blob/7dc5e56f6e4d83f0ad03a395120e9a2bbcbafc41/builder/core.py#L203) bütün null alanları siliyordu; `enum=null` gibi desteklenmeyen kısıt sessizce kaybolabiliyordu. `required=null` TypeError veriyordu. | Yalnız açıklama/başlık gibi boş metaveri temizlenir. Geçersiz kısıt ve required listesi açık `ContractError` ile reddedilir. |
| P2 | [Yanıt şeması okuma](https://github.com/Mehmetalimans/freya-builder/blob/7dc5e56f6e4d83f0ad03a395120e9a2bbcbafc41/builder/core.py#L101) null medya türü/özellik tanımında AttributeError verebiliyordu. | Her seviyede nesne kontrolü eklendi; kimlik başarı sinyali yoksa belgeli fallback, kapanış sinyali yoksa açık sözleşme hatası kullanılır. |
| P2 | "100 senaryo" testlerinin çoğu gerçek diyalog yerine belirli cümlelerin varlığını kontrol ediyordu; bazıları yukarıdaki hatalı talimatları zorunlu kılıyordu. | 16 çalıştırılabilir takvim/şema kontrolü korundu; metin tekrarı kontrollerinin yerine 13 sentetik regresyon testi eklendi. Test sayısı başarı ölçüsü olarak kullanılmıyor. |

Miraç'ın yararlı değişiklikleri korundu: Monday-through-Friday ve tireli bant
desteği, boş açıklama alanları, hook mekanizması, leap-year/sınır testleri.
`connect_retries=2` de korundu: [resmî kit](../starter-v3/build-the-builder/docs/tools-and-code.md)
bunu yalnız bağlantı kurulmadan önceki TCP/TLS hatalarının tekrarı olarak tanımlar;
HTTP hatalarını veya timeout'u tekrarlamaz. `config.maxRetries=0` değişmedi.
Bu ayarı çift banka kaydı oluşturan bir HTTP retry olarak nitelemek doğru olmaz.

## Doğrulama

- Miraç'ın son commit'inde mevcut 161 yerel test geçti; buna rağmen yeni
  regresyon paketinin 13 testinden 11'i hata yakaladı (alt senaryolar dahil
  23 başarısız assertion, 2 hata). Aynı paket düzeltilen kodda 13/13 geçti.
- Düzeltme sonrasında toplam 90 yerel test geçti. [Önce/sonra kanıtı](../reports/mirac-review-regressions.json)
  ve [test çıktısı](../reports/unit-tests.txt) saklanır.
- 0.1.10 adayının temiz, pip içermeyen Python 3.12.14 ortamındaki doğrulama
  sonucu, A ve A+B tekrar hash'leri ve kesin arşiv
  [temiz ortam raporunda](../reports/verification.json) kaydedilir.
- Miraç'ın önceki Python 3.13.5 paket raporu [tarihsel kopyada](../reports/history/mirac-7dc5e56-verification.json)
  korundu; yeni sürümün kanıtı olarak kullanılmaz.

Bu ilk kod incelemesi Freya çağrısı, dağıtım veya ücretli test başlatmadı. O aşamada 0.1.10'un canlı
başarısı bilinmiyor; platformdaki önceki 0.1.9 workflow'u değişmedi. Birim testleri
telefon modelinin talimatlara uyduğunu veya yeni sürümün daha yüksek puan
alacağını kanıtlamaz. Yeni hook'ların canlı yayın/export/geri okuma doğrulaması
da henüz yapılmadı.

## Ekip raporundaki kanıt sınırları

`docs/teammate-sync.md` içindeki canlı %100 başarı, gecikme ve maliyet ifadeleri
Miraç'ın bildirimidir. Bu dalda bunları yeniden doğrulayacak koşu/tekrar kimlikleri,
workflow hash'leri ve birleşik scorer dosyaları yok; doğrulanmış ortak skor olarak
sunulmamalı. Kaynak rapor korunup üstüne bu açıklama eklendi.

Raporda B'nin üç public vakasının da ekip tarafından çalıştırıldığı belirtiliyor.
Dolayısıyla bunlar artık **ekip genelinde kullanılmamış holdout** sayılamaz;
tekrarları regresyon ölçümüdür. Yerel `--split holdout` seçimi eski vaka ayrımını
korur, verinin bağımsızlığını garanti etmez. Kalan üç A vakasının ekip genelindeki
kullanım geçmişi doğrulanmadan onlar için de bağımsızlık iddia edilmemeli.
İncelemede holdout vaka dosyaları veya konuşmaları açılmadı; bildirilen sonuçlar
kod/prompt düzeltmesinde kullanılmadı.

Sonraki adım: bekleyen önceki değerlendirme kaydını uzlaştır; 0.1.10'u gerçek
Freya validate/publish/readback yoluyla doğrula; geliştirme kümesinde tekrarlı
ölç; kullanılan B vakalarını bağımsız genelleme testi olarak etiketleme.

Bu sonraki adımlar 10 Ekim'deki canlı çalışmada başlatıldı: 0.1.9 kaydı
kurtarıldı, 0.1.10 yayın/geri okuması ve 21 çağrılık testi tamamlandı.
Güncel sonuç ve ek düzeltmeler [canlı doğrulama kaydındadır](live-validation.md).
