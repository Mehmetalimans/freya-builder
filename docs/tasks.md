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
görüldü. Bu, resmî `builder/runtime.py` dağıtım doğrulamasının veya benchmark
başarısının yerine geçmez. Miraç workspace'inde henüz simülasyon yapılmadı;
10 Ekim'de görülen $100 bakiye harcanmış tutar değildir.

| Sahip | İş | Durum / kabul ölçütü |
| --- | --- | --- |
| Kullanıcı | Brief + OpenAPI okuma, workflow üretimi (`builder/core.py`) | Çevrimdışı baseline var; 29 birim testi ve temiz ortam A/A+B üretimi geçti. |
| Kullanıcı | Geliştirme vakalarından genel hata analizi ve otomatik düzeltme | İlk gerçek resmî başarısızlık, maliyet ve süre görülünce başlanacak; henüz uygulanmadı. |
| Arkadaş | Miraç Freya workspace'inde `builder/runtime.py` dağıtımını doğrulama | UI yayımı v3 doğrulandı; programatik `deployed_verified` ve gerçek `workflow.export.json` kanıtı hâlâ gerekli. Başka takım workspace'i teslim için kullanılmaz. |
| Arkadaş | `builder/evaluate.py` ile resmî public geliştirme vakalarını ölçme | Önce maliyet üst sınırı ve tek aktif simülasyon teyidi. `evaluation.json` status=measured, vaka bazlı sonuç, süre ve maliyet kanıtı. |
| Arkadaş | Hata/timeout ve sonuç kaydı | Araç hatası, uzakta hâlâ çalışan iş olasılığı ve hesaplanan/gerçek maliyet ayrı. Belirsiz toplam `null`. |
| Ortak | `builder/build.py`, sözleşme, bütçe, sürüm | Değişiklik için ilgili iki parça testi ve PR incelemesi. |
| Ortak | Ayrılmış 3 A + 3 B public vaka ile genelleme | Geliştirme sabitlendikten sonra üç tekrar; gizli final skoru iddiası yok. |
| Ortak | Temiz ortam, son commit, iki export + iz ve resmî teslim | `scripts/release.py`, `scripts/verify_release.py`; eksik final verileri tamamlanmadan teslim edildi sayılmaz. |

## Sıradaki çalışma sırası

1. İş bölümü PR'si açıldı, çevrimdışı GitHub kontrolü geçti. `mbirlik24`
   daveti kabul edince her bilgisayarda ayrı klon/dal ve PR incelemesi.
2. Arkadaş Miraç workspace'inde kendi yerel Freya erişimini ve resmî kit dağıtımını doğrular.
3. Gerçek harcama üst sınırı/tek operatör kesinleşince küçük resmî geliştirme
   ölçümü; sonuç üretim tarafına `docs/contracts.md` biçiminde iletilir.
4. Kullanıcı genel üretim hatalarını düzeltir. Geliştirmede kullanılmamış public
   vakalarla ayrı kontrol; başarısı ölçülmemiş özellik iddiası yok.
5. Son commit ve temiz ortam tekrarı; organizatörün güncel katılımcı e-postası
   ve teslim bağlantısı doğrulanır.

Arkadaşın kendi AI aracına verilecek kısa başlangıç metni
[teammate-start.md](teammate-start.md) içindedir.
