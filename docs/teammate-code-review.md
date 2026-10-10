# Antigravity dalı incelemesi — 10 Ekim 2026

İncelenen dal: `feat/agent-core-optimization`, commit
`daef83b` (öncesindeki beş geliştirme commit'i dahil). Dal fetch edildi ve
korundu; mevcut yerel değişikliklerin üzerine yazılmadı. Aşağıdaki davranışlar
incelenmeden ana dala taşınmamalı. Holdout vaka metinleri/sonuçları bu incelemede
okunmadı; inceleme üretici kodu, bütçe ve test yapısıyla sınırlandı.

| Öncelik | Bulgu | Bu daldaki karşılık |
| --- | --- | --- |
| P1 | `budget.json` 0,10 USD vaka tavanını "verified" sayıyor; kanıt olarak yalnız 200 kredi × 0,5 USD bakiyesini veriyor. Bakiye vaka fiyatını kanıtlamaz. | Doğrulanmış vaka fiyatı `null`; açık kullanıcı iznine dayalı, bakiyeyi izleyen sınırlı kampanya. |
| P1 | Takvim çıkarımı brief'teki bütün ISO tarihlerini tatil sayıyor; örnek `now` tarihi de buna dahil olabilir. Ayrıca 14 Ekim'e özel tarih/son gün örnekleri her çağrıya ekleniyor. | Yalnız tanınan tatil tanımındaki tarihler alınır; çağrıdaki `now` üzerinden hesaplanır. Farklı yıl/tatil/bant testleri var. |
| P1 | `create_promise` sonrası hook ilk başarılı ürünün ardından çağrıyı kapatmayı emrediyor. Çok ürünlü çağrıda kalan sözler/notlar atlanabilir. | Ürünler ve kapanış tam brief'e göre sürer; tek başarılı kayıt otomatik terminal koşulu değildir. |
| P1 | Callback ve transfer hook'ları `ok` kontrol etmeden başarı duyuruyor; transfer kapanışı için `chosen_queue` diye enum dışı yer tutucu veriliyor. | Başarı bankanın sonucuyla doğrulanır, kapanış enum'ları araç şemasından gelir. |
| P1 | Her kimlik API hatasını yanlış müşteri cevabı saymak, gerçek 500/timeout hatalarında hatalı ret yaratır. | `verified=false` normal kimlik reddi ile araç istisnası ayrı; canlı turda beş gerçek araç istisnası kaydedildi. |
| P2 | Güvenlik alanları, üç yanlış cevap, bant eşikleri ve callback saatleri sabit prompt kurallarıyla yineleniyor. Görülmemiş brief bunları değiştirebilir. | Tam girdi korunur; desteklenen takvim/bant tabloları girdiden çıkarılır. Tanınmayan tanımlar açık sınırlama olarak kaydedilir. |

Belgeli `post_process_code` mekanizması yararlı bir yaklaşım olabilir; mevcut
hook'ların yanlış iş kararlarıyla topluca alınması uygun değil. Hook fikriyle
hook'un politika doğruluğu aynı şey değildir. Mevcut dal geçmişi değiştirilmedi;
sonraki birleştirmede bu bulgular üzerinden ayrı kod incelemesi yapılmalı.
