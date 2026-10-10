# İki kişilik görev takibi

Son güncelleme: 10 Ekim 2026. Durumlar yalnız bu repodaki kanıta dayanır.
Ortak özel depo `Mehmetalimans/freya-builder`; geliştirme dalı → pull request →
diğer kişinin incelemesi → ana dal sırasıyla çalışılır. GitHub kullanıcı adı
bilinmeyen ekip arkadaşına henüz erişim daveti gönderilmedi.

| Sahip | İş | Durum / kabul ölçütü |
| --- | --- | --- |
| Kullanıcı | Brief + OpenAPI okuma, workflow üretimi (`builder/core.py`) | Çevrimdışı baseline var; 29 birim testi ve temiz ortam A/A+B üretimi geçti. |
| Kullanıcı | Geliştirme vakalarından genel hata analizi ve otomatik düzeltme | İlk gerçek resmî başarısızlık, maliyet ve süre görülünce başlanacak; henüz uygulanmadı. |
| Arkadaş | Yeni **takım** Freya workspace'inde `builder/runtime.py` dağıtımını doğrulama | Kimlik bilgileri yalnız yerel süreçte; `deployed_verified` ve gerçek `workflow.export.json` kanıtı gerekli. Başka takım workspace'i teslim için kullanılmaz. |
| Arkadaş | `builder/evaluate.py` ile resmî public geliştirme vakalarını ölçme | Önce maliyet üst sınırı ve tek aktif simülasyon teyidi. `evaluation.json` status=measured, vaka bazlı sonuç, süre ve maliyet kanıtı. |
| Arkadaş | Hata/timeout ve sonuç kaydı | Araç hatası, uzakta hâlâ çalışan iş olasılığı ve hesaplanan/gerçek maliyet ayrı. Belirsiz toplam `null`. |
| Ortak | `builder/build.py`, sözleşme, bütçe, sürüm | Değişiklik için ilgili iki parça testi ve PR incelemesi. |
| Ortak | Ayrılmış 3 A + 3 B public vaka ile genelleme | Geliştirme sabitlendikten sonra üç tekrar; gizli final skoru iddiası yok. |
| Ortak | Temiz ortam, son commit, iki export + iz ve resmî teslim | `scripts/release.py`, `scripts/verify_release.py`; eksik final verileri tamamlanmadan teslim edildi sayılmaz. |

## Sıradaki çalışma sırası

1. İlk depo push'u ve iş bölümü PR'si; ikinci kişinin GitHub kullanıcı adıyla
   private erişim daveti ve her bilgisayarda ayrı klon/dal.
2. Arkadaş kendi hesabının Freya erişimini ve resmî kit dağıtımını doğrular.
3. Gerçek harcama üst sınırı/tek operatör kesinleşince küçük resmî geliştirme
   ölçümü; sonuç üretim tarafına `docs/contracts.md` biçiminde iletilir.
4. Kullanıcı genel üretim hatalarını düzeltir. Geliştirmede kullanılmamış public
   vakalarla ayrı kontrol; başarısı ölçülmemiş özellik iddiası yok.
5. Son commit ve temiz ortam tekrarı; organizatörün güncel katılımcı e-postası
   ve teslim bağlantısı doğrulanır.

Arkadaşın kendi AI aracına verilecek kısa başlangıç metni
[teammate-start.md](teammate-start.md) içindedir.
