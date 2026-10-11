# Miraç son push incelemesi — 11 Ekim 2026

İncelenen uç: `origin/integration/v3-final`,
`3d731be8eca4f1c815b68fe5d9b0fe68e1e3a831`.
Son dört commit: `99b87e5`, `37d48a4`, `6dbc0a1`, `3d731be`.
`5494a2e` sonrasındaki 12 dosyanın değişiklikleri, kalıtılan kritik
kod ve bizim mevcut yerel değişiklikler karşılaştırıldı. Kaynak ayrı
scratch arşivinde incelendi; mevcut checkout üzerine alınmadı.
Bu inceleme canlı test, yayın veya ücretli model çağrısı başlatmadı.

## Doğrulama

- Miraç'ın mevcut kendi testleri: **181/181 geçti**.
- Aynı kaynakta bizim 13 davranış regresyonu: alt senaryolar dahil
  **16 başarısız assertion, 3 hata**. Test sayısı ile alt kontrol sayısı farklıdır.
- Bizim mevcut checkout: **109/109 yerel test geçti**. Son dört dosya değişikliği
  henüz commit edilmemiştir; bu kontroller canlı başarı kanıtı değildir.
- Sentetik hook ve bütçe örnekleri aşağıdaki iki P1 bulgusunu tekrar üretti.
  Bunlar gerçek bir müşteri veya gerçekleşmiş harcama değildir.
- Ham test çıktıları ve sentetik kanıt `runs/final-preflight/review-*` altında
  yerel kalır. Önceki yerel değişikliklerin yaması
  `handoff/review-before-approval.patch` dosyasına korundu.

## Bulgular

| Öncelik | Bulgu | Somut kanıt / etkisi |
|---|---|---|
| P1 | Bankanın kimlik tamamlama kararı yerelde değiştiriliyor | [core.py:265](https://github.com/Mehmetalimans/freya-builder/blob/3d731be8eca4f1c815b68fe5d9b0fe68e1e3a831/builder/core.py#L265) sayaç artırıyor, 269. satır `all_verified=True` yazıyor. Aynı tek kontrolün iki kez başarılı yanıtını kalıcı `vars` ile verdiğimde bankanın False değeri True oldu. Farklı gerekli soruların tamamlandığı kanıtlanmıyor. Vars kalıcı değilse de vaat edilen sayaç garantisi çalışmaz. |
| P1 | 100 USD harcama izni tüketimle karşılaştırılmıyor | [campaign.py:18](https://github.com/Mehmetalimans/freya-builder/blob/3d731be8eca4f1c815b68fe5d9b0fe68e1e3a831/builder/campaign.py#L18) cap için 300 USD kabul ediyor; reserve gerçek gözlenen tüketimi cap'e karşı durdurmuyor. Sentetik 244,93 USD başlangıç ve 130 USD bakiye, 114,93 USD tüketim olmasına rağmen yeni koşuyu kabul etti. Büyük bakiye kullanıcının 100 USD yetkisini artırmaz. |
| P1 | Politika parser'ı konuları karıştırıyor ve public varsayımlarını kullanıyor | [core.py:138](https://github.com/Mehmetalimans/freya-builder/blob/3d731be8eca4f1c815b68fe5d9b0fe68e1e3a831/builder/core.py#L138): ödeme için iki deneme, kimlik için dört yanlış cevap verilen sentetik metinde kimlik limitini 2 çıkardı. Tanınmayan tabloda public bantlar; tanınmayan saatlerde 10:00–19:00; güvenlik soru sayısında 2 varsayılıyor. Bunlar görülmemiş görev için doğrulanmış kurallar değildir. |
| P2 | Transfer kuyruğu kapanış nedeni gibi kullanılıyor | [core.py:537](https://github.com/Mehmetalimans/freya-builder/blob/3d731be8eca4f1c815b68fe5d9b0fe68e1e3a831/builder/core.py#L537) ve 646: `reason=queue`. Resmî A kuralı 42'de queue=general, reason=human. Bu talimat aynı promptta doğru kuralla çelişiyor. İşlem sırası fikri korunabilir; nedeni verilen politika belirlemeli. |
| P2 | Kayıt bildirimi monitoring'e çevrilmiş | [core.py:603](https://github.com/Mehmetalimans/freya-builder/blob/3d731be8eca4f1c815b68fe5d9b0fe68e1e3a831/builder/core.py#L603) `this call is monitored` diyor. Görev, çağrının kayda alındığının bildirilmesini istiyor. Monitoring kaydın açık bildirimi olarak güvenilir değildir; quoted zorunlu metinler de korunmalı. |
| P2 | C/D/E fixture'ları tool sözleşmesiyle tam uyumlu değil | C, hardship transfer kuyruğu istiyor; mevcut v3 API yalnız restructuring/general/support içeriyor. D/E testleri yalnız transfer enum'unu değiştiriyor; legal_counsel/unemployed/fraud_claim gibi yeni add_note nedenleri API'de yok. Bu testler yalnız derleme/assertion; gerçek telefon/banka başarısını ölçmüyor. B ayrıca tek başına derleniyor; resmî B, A'ya eklenmeli. |
| P2 | Rapor son kaynakla eşleşmiyor | Son rapor A hash'i 5effc0a…; mevcut A üretimi a5af7d43… . B raporu f8cc4b1…; mevcut A+B üretimi 4ba99e01… . Unit raporu 163 test, mevcut kaynakta 181 test var. Güncel sürüm hâlâ 0.1.9. Commit başlığındaki 7/7 iddiasını son kaynak hash'i ve üç tekrar banka/judge kanıtı olmadan son sürüme atfedemiyoruz. |
| P2 | Önceki null/boolean problemleri sürüyor | Ek regresyonlarda string `false` başarı gibi ele alınabiliyor; bozuk/null şema metadatası beklenen ContractError yerine TypeError/AttributeError üretiyor. Son push bunların tamamını düzeltmemiş. |

Belirsiz tarih için ayrı action/date çıkarım promptları ve sentetik politika
çeşitliliği yararlı yönlerdir. Onaylı uygulamada güvenlik bayrağını değiştiren
sayaç, sabit politika varsayımları ve genişleyen harcama kabulü taşınmamalı.

## Ortak çalışma ve kalan gerçek durum

PR #6 şu an GitHub'da çatışmalı. Bizim dal remote'a göre dört commit ileride,
ayrıca evaluate/recover/sonuç özeti/test dosyalarında dört korunmuş yerel
değişiklik var. Yeni birleştirme bunları koruyarak yapılmalı; main'e doğrudan
push yapılmamalı. Yeni helper'ların yalnız birim testi, canlı doğrulama yerine
kullanılmamalı.

Son yerel canlı kayıt: 0.1.13 A dev 7/7, kalan A 2/3; B ölçümü tamamlanmadı.
B'de bir `inconclusive` etiketine rağmen olumlu açıklama var; etiket başarıya
çevrilmedi. `state/budget-ledger.json` bu B koşusunu hâlâ bekleyen rezerv
olarak tutuyor. Onaylı uygulama öncesi uzak durum ve mevcut banka kayıtları
salt okunur uzlaştırılmalı; rezerv körlemesine silinmemeli.

Duygu etiketi olmayan çağrılar için memnuniyet oranı ölçülemedi. Nazik iletişim
talimatı bizim adayda var; bu, müşterinin memnun kaldığını ispatlamaz.

## Onaya sunulan 30 dakikalık kapsam

| Süre | İş | Çıkış koşulu |
|---|---|---|
| 0–5 dk | Yerel değişiklikleri sabit kayıtla koru; kritik dosyaları seçerek Git çatışmasını çöz; workspace/test ve bekleyen bütçe durumunu kontrol et. | Tek ortak aday; gerçek 100 USD sınırı; test çakışması ve belirsiz rezerv çözülmeden ücretli başlatma yok. |
| 5–14 dk | Sahte all_verified üretimini kaldır; 100 USD tüketim kontrolünü koru; transfer nedenini politika/şemaya bırak; kayıt bildirimini düzelt. Mevcut tarih/ikna/nazik iletişim korumalarını koru. | Regresyonlar geçer; bankanın doğrulama bayrağı değiştirilmez. |
| 14–25 dk | Temiz ortam kontrolü; yayın/export/geri okuma; en çok altı hedefli public vaka birer tekrar: kimlik, hardship/transfer, belirsiz tarih, tool fault, multi-product ikna, multi-product tarih. | Gerçek verdict + banka kaydı, süre, araç hatası ve bakiye kaydı. Inconclusive/timeout başarı sayılmaz. |
| 25–30 dk | Son kaynak/hash/raporu kaydet, gizli bilgi kontrolü yap, PR dalına gönder ve kısa durum ver. | Kesin commit ve yeniden çalıştırma komutu; main merge ekip incelemesine bağlı. |

Bu kapsam yeni özellik veya tüm public vakaların üç tekrarını vaat etmez.
Platform beklemesi süreyi aşarsa 30. dakikada tamamlanan/eksik kayıt açıkça
raporlanır; devam eden çağrıların bittiği varsayılmaz. Etkinliğin kayıtlı
takviminde gizli brief'ler bugün 20:00 İstanbul'da açılıyor; kod düzeltmeleri
ilk bölümde sabitlenmeli, gizli brief'ten kural/değer koda eklenmemeli.

Tarihsel plan kullanıcı tarafından onaylandı. Eski 100 USD sınırı ayrıca
kaldırıldı; mevcut workspace deneme kredisine izin verildi. Uygulama 0.1.15'te
tamamlandı; son canlı ölçüm aşaması kullanıcı tarafından beş dakikaya kısaltıldı.
Gerçek sonuç ve kalan sınırlamalar [approved-quick-checks.md](approved-quick-checks.md).
