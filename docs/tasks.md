# İki kişilik görev takibi

Son güncelleme: 10 Ekim 2026. Durumlar yalnız bu repodaki kanıta dayanır.
Güncel geniş test: 19 gerçek çağrı (önceki pilot hariç); 17'si birleşik scorer
ile puanlandı, son ikisinin ledger okuması servis 500/1101 hatasında engellendi.
En iyi tamamlanmış geniş tur 0.1.6 ile 6/7; 0.1.9 adayının tam skoru bilinmiyor.
Kanıt ve sürüm ayrımı: [ölçüm ve açık işler özeti](evaluation-summary.md),
`reports/extended-evaluation.json`, `docs/extended-test-notes.md`.
Aşağıdaki ilk pilot bilgileri tarihsel kayıttır.
Ortak özel depo `Mehmetalimans/freya-builder`; geliştirme dalı → pull request →
diğer kişinin incelemesi → ana dal sırasıyla çalışılır. `mbirlik24` yazma
erişimi doğrulandı. GitHub kişisel private depoda dal korumasını
bu planda uygulamıyor; zorunlu PR incelemesi ekip sürecidir.

Çalışma hedefi artık [Mirac Birlik's Workspace](https://staging-app.freyavoice.ai/?workspaceId=8783bb12-56fc-489a-8608-590676971f6c).
Buildo denemesi bırakıldı. Brief A'nın çevrimdışı üretilen tanımı Miraç
workspace'inde [Brief A - Builder Baseline v3](https://staging-app.freyavoice.ai/workflow/82c69318-2c6a-43d3-9661-a93ea8b9b99d?workspaceId=8783bb12-56fc-489a-8608-590676971f6c)
olarak UI üzerinden yayımlandı. Yeniden yüklenmiş JSON'da `identity`,
`collection`, `finished` düğümleri ile `experimental-5` sağlayıcı/modeli
görüldü. Ardından builder 0.1.3 ile aynı workflow API üzerinden **v4** olarak
yayımlandı, resmî export ve davranış geri okuması `deployed_verified` oldu.
Kanıt `runs/20261010T143548Z-dcb3f232/` altında. İlk resmî geliştirme ölçümü
tamamlandı: **PUB-01 1/1 geçti**, simülasyon 41 saniye, gözlenen bakiye farkı
0,01995 USD. O pilotun sonunda görülen bakiye 99,8602 USD idi; ayrıntı
`reports/first-live-evaluation.json` içinde. Sonraki geniş turlar yukarıdaki
özette kayıtlıdır. En son kayıtlı bakiye 98,83555 USD; yeni bakiye sorgusu değildir.
Son aday 0.1.9 aynı workflow'un API üzerinden doğrulanmış v10 sürümüdür;
üç tekrar ve holdout hâlâ bekliyor.

| Sahip | İş | Durum / kabul ölçütü |
| --- | --- | --- |
| Kullanıcı | Brief + OpenAPI okuma, workflow üretimi (`builder/core.py`, `builder/calendar.py`) | Kimlik yanıtı ve takvim/ürün son tarihi düzeltmeleri uygulandı; 0.1.9 adayının tam canlı ölçümü servis düzelmesini bekliyor. |
| Kullanıcı | Geliştirme vakalarından genel hata analizi ve otomatik düzeltme | Hatalar incelendi, birkaç aday karşılaştırıldı. Genel otomatik onarım motoru henüz yok; düzeltmeler asistan tarafından geliştirildi. |
| Arkadaş | Miraç Freya workspace'inde `builder/runtime.py` dağıtımını doğrulama | Tamamlandı: son aday 0.1.9 için API doğrulama/yayınlama/export/geri okuma v10. Anahtar-workspace kontrolü otomatik. |
| Arkadaş | `builder/evaluate.py` ile resmî public geliştirme vakalarını ölçme | Geniş ölçümler raporda. Son iki çağrı tamamlandı fakat puanlanamadı; `builder/recover.py` salt okuma kurtarması ve bekleyen rezerv var. Tek test operatörü bu oturumdaki asistan. |
| Arkadaş | Hata/timeout ve sonuç kaydı | Araç hatası, uzakta hâlâ çalışan iş olasılığı ve hesaplanan/gerçek maliyet ayrı. Belirsiz toplam `null`. |
| Ortak | `builder/build.py`, sözleşme, bütçe, sürüm | Değişiklik için ilgili iki parça testi ve PR incelemesi. |
| Ortak | Ayrılmış 3 A + 3 B public vaka ile genelleme | Geliştirme sabitlendikten sonra üç tekrar; gizli final skoru iddiası yok. |
| Ortak | Temiz ortam, son commit, iki export + iz ve resmî teslim | `scripts/release.py`, `scripts/verify_release.py`; eksik final verileri tamamlanmadan teslim edildi sayılmaz. |

## Sıradaki çalışma sırası

1. İş bölümü PR'si açıldı; `mbirlik24` yazma erişimi doğrulandı. Her bilgisayarda ayrı klon/dal ve PR incelemesi.
2. API dağıtımı tamam. Kullanıcı bu oturumda test operatörü olarak asistanı seçti;
   arkadaş aynı anda simülasyon başlatmamalı. Banka anahtarı sabit ve yerel tutulmalı.
3. Banka ledger servisi düzeldiğinde son tamamlanan turu yeni simülasyon açmadan
   kurtar. Sonra güncel adayın yedi geliştirme vakasını ve üç tekrar tutarlılığını ölç.
   Fiyat belirsizliği ve açık kampanya izni [cost-analysis.md](cost-analysis.md) içinde.
4. Kullanıcı genel üretim hatalarını düzeltir. Geliştirmede kullanılmamış public
   vakalarla ayrı kontrol; başarısı ölçülmemiş özellik iddiası yok.
5. Son commit ve temiz ortam tekrarı; kickoff e-postası işlendi, ayrıca geleceği
   belirtilen teslim adımları/bağlantısı hâlâ bekleniyor.
6. Arkadaşın `feat/agent-core-optimization` dalını birleştirmeden önce
   [kod incelemesi](teammate-code-review.md) bulgularını çöz. Sabit örnekleri ve
   doğrulanmamış vaka fiyatını geri getirme; iki taraftaki kodu ezme.

Arkadaşın kendi AI aracına verilecek kısa başlangıç metni
[teammate-start.md](teammate-start.md) içindedir.
