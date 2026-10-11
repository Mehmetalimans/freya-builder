# İki kişilik görev takibi

Son güncelleme: 11 Ekim 2026. Durumlar yalnız bu repodaki kanıta dayanır.
Canlı Freya simülasyonları:
- **Brief A (v10):** 7/7 (%100 Başarı) — Happy path, callback, identity, dates/tatil atlama, hardship, amounts tümü geçti (`runs/20261011T162746Z-2c679007/evaluation.json`).
- **Brief B (v10):** 3/3 (%100 Başarı) — PUB-11, PUB-12, PUB-13 çoklu ürün, ikna limitleri ve not kuralları geçti (`runs/20261011T164608Z-8ac4a608/evaluation.json`).
- **Bakiye & Maliyet:** İki tam canlı değerlendirme turunda toplam ~0.43 USD kredi harcandı; kalan bakiye ~240.93 USD (20 USD güvenlik tamponu eksiksiz korundu).
Ortak özel depo `Mehmetalimans/freya-builder`; geliştirme dalı → pull request →
diğer kişinin incelemesi → ana dal sırasıyla çalışılır. `mbirlik24` yazma
erişimi doğrulandı. GitHub kişisel private depoda dal korumasını
bu planda uygulamıyor; zorunlu PR incelemesi ekip sürecidir.

Çalışma hedefi [Mirac Birlik's Workspace](https://staging-app.freyavoice.ai/?workspaceId=8783bb12-56fc-489a-8608-590676971f6c).
Brief A `practice-a` slotunda (v10), Brief B `practice-b` slotunda (v10) olarak
yayımlandı ve doğrulandı. Resmî export ve geri okuma kontrolleri eksiksiz geçti.

| Sahip | İş | Durum / kabul ölçütü |
| --- | --- | --- |
| Kullanıcı | Brief + OpenAPI okuma, workflow üretimi (`builder/core.py`, `builder/calendar.py`) | Kimlik yanıtı ve takvim/ürün son tarihi düzeltmeleri uygulandı; 0.1.9 adayının tam canlı ölçümü servis düzelmesini bekliyor. |
| Kullanıcı | Geliştirme vakalarından genel hata analizi ve otomatik düzeltme | Hatalar incelendi, birkaç aday karşılaştırıldı. Genel otomatik onarım motoru henüz yok; düzeltmeler asistan tarafından geliştirildi. |
| Arkadaş | Miraç Freya workspace'inde `builder/runtime.py` dağıtımını doğrulama | Tamamlandı: API doğrulama/yayınlama/export/geri okuma v4. Anahtar-workspace kontrolü otomatik. |
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
