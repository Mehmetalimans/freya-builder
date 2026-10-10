# İki kişilik görev takibi

Son güncelleme: 10 Ekim 2026. Durumlar yalnız bu repodaki kanıta dayanır.
Ortak özel depo `Mehmetalimans/freya-builder`; geliştirme dalı → pull request →
diğer kişinin incelemesi → ana dal sırasıyla çalışılır. `mbirlik24` daveti
gönderildi, kabul bekleniyor. GitHub kişisel private depoda dal korumasını
bu planda uygulamıyor; zorunlu PR incelemesi ekip sürecidir.

Çalışma hedefi artık [Mirac Birlik's Workspace](https://staging-app.freyavoice.ai/?workspaceId=8783bb12-56fc-489a-8608-590676971f6c).
Buildo denemesi bırakıldı. Brief A'nın çevrimdışı üretilen tanımı Miraç
workspace'inde [Brief A - Builder Baseline v3](https://staging-app.freyavoice.ai/workflow/82c69318-2c6a-43d3-9661-a93ea8b9b99d?workspaceId=8783bb12-56fc-489a-8608-590676971f6c)
olarak UI üzerinden yayımlandı. Yeniden yüklenmiş JSON'da `identity`,
`collection`, `finished` düğümleri ile `experimental-5` sağlayıcı/modeli
görüldü. Ardından builder 0.1.3 ile aynı workflow API üzerinden **v4** olarak
yayımlandı, resmî export ve davranış geri okuması `deployed_verified` oldu.
Kanıt `runs/20261010T143548Z-dcb3f232/` altında. Miraç workspace'inde bu çalışma
henüz simülasyon başlatmadı. API 100 USD bakiye ve toplam 0 kredi kullanım
gösteriyor; bu gelecek simülasyon tarifesi değildir.

| Sahip | İş | Durum / kabul ölçütü |
| --- | --- | --- |
| Kullanıcı | Brief + OpenAPI okuma, workflow üretimi (`builder/core.py`) | Çevrimdışı baseline var; 31 birim testi geçti; davranış başarısı ölçülmedi. |
| Kullanıcı | Geliştirme vakalarından genel hata analizi ve otomatik düzeltme | İlk gerçek resmî başarısızlık, maliyet ve süre görülünce başlanacak; henüz uygulanmadı. |
| Arkadaş | Miraç Freya workspace'inde `builder/runtime.py` dağıtımını doğrulama | Tamamlandı: API doğrulama/yayınlama/export/geri okuma v4. Anahtar-workspace kontrolü otomatik. |
| Arkadaş | `builder/evaluate.py` ile resmî public geliştirme vakalarını ölçme | Önce maliyet üst sınırı ve tek aktif simülasyon teyidi. `evaluation.json` status=measured, vaka bazlı sonuç, süre ve maliyet kanıtı. |
| Arkadaş | Hata/timeout ve sonuç kaydı | Araç hatası, uzakta hâlâ çalışan iş olasılığı ve hesaplanan/gerçek maliyet ayrı. Belirsiz toplam `null`. |
| Ortak | `builder/build.py`, sözleşme, bütçe, sürüm | Değişiklik için ilgili iki parça testi ve PR incelemesi. |
| Ortak | Ayrılmış 3 A + 3 B public vaka ile genelleme | Geliştirme sabitlendikten sonra üç tekrar; gizli final skoru iddiası yok. |
| Ortak | Temiz ortam, son commit, iki export + iz ve resmî teslim | `scripts/release.py`, `scripts/verify_release.py`; eksik final verileri tamamlanmadan teslim edildi sayılmaz. |

## Sıradaki çalışma sırası

1. İş bölümü PR'si açıldı, çevrimdışı GitHub kontrolü geçti. `mbirlik24`
   daveti kabul edince her bilgisayarda ayrı klon/dal ve PR incelemesi.
2. API dağıtımı tamam. Kullanıcı bu oturumda test operatörü olarak asistanı seçti;
   arkadaş aynı anda simülasyon başlatmamalı. Banka anahtarı sabit ve yerel tutulmalı.
3. Kullanıcının istediği fiyat analizi [cost-analysis.md](cost-analysis.md) içinde.
   Gerçek harcama üst sınırı kesinleşince `--only` ile küçük resmî geliştirme
   ölçümü; sonuç üretim tarafına `docs/contracts.md` biçiminde iletilir.
4. Kullanıcı genel üretim hatalarını düzeltir. Geliştirmede kullanılmamış public
   vakalarla ayrı kontrol; başarısı ölçülmemiş özellik iddiası yok.
5. Son commit ve temiz ortam tekrarı; kickoff e-postası işlendi, ayrıca geleceği
   belirtilen teslim adımları/bağlantısı hâlâ bekleniyor.

Arkadaşın kendi AI aracına verilecek kısa başlangıç metni
[teammate-start.md](teammate-start.md) içindedir.
