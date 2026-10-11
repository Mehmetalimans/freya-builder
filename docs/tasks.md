# Devir güncellemesi — 11 Ekim 21:05 İstanbul

Kullanıcı mevcut çalışmanın sonuçlandırılmasını, GitHub'a pushlanmasını ve sonrasında Miraç'ın devam etmesini istedi. Güncel dal `final/case-folder-builder`, taslak PR #7. Teknik durum ve sonraki adımlar `docs/mirac-final-handoff.md` dosyasında tamamlanacak. Bu oturum devirden sonra simülasyon veya workflow değişikliği başlatmayacak.

# Final görev durumu — 11 Ekim 20:39 İstanbul

Kullanıcı bütün teknik yürütmeyi bu oturuma verdi. Miraç'ın paralel değişiklik yapmadığı varsayımıyla ayrı `final/case-folder-builder` dalında çalışılıyor; main'e doğrudan push yok.

- Tamam: güncel vaka belgeleri alındı; eski BRIEF saklandı; 34 sentetik müşteri ve 617 servis cevabı için yerel sözleşme kontrolü geçti.
- Devam: Cloudflare yayın ve HTTPS kontrolü, genel klasör builder'ının sabitlenmesi.
- Sırada: kaydı tutulan gerçek üretim, Freya doğrulama/export, altı örnek ve ek hata senaryolarının ölçümü, temiz ortam ve teslim paketi.
- E-posta: kullanıcı ayrıca gönderim onayı verecek. Miraç adresi mbirlik24@ku.edu.tr; Mehmet adresi mmansuroglu24@ku.edu.tr. Takım etiketi son onayda doğrulanacak.

Aşağıdaki kayıtlar practice geçmişidir.

# İki kişilik görev takibi

**11 Ekim güncellemesi:** Kullanıcı son testleri sürdürdü. Güncel aday
0.1.13, A workflow v13. Önceki kesilen tur salt okunur kurtarıldı: 6/7.
104 yerel test geçti; son public A/B ölçümü sürüyor. Yeni işlerin kanıtı
[final-checks.md](final-checks.md) içinde; aşağıdaki ara kaydı tarihseldir.

Dil kontrolü tamamlandı: resmî yarışma İngilizce/metin; kod mevcut haliyle
uyumlu. Yeni sesli ayar veya ücretli test açılmadı.
Git kontrolünde `integration/v3-final` dalında üç yeni Miraç commit'i görüldü:
`1aefb49`, `803203f`, `5494a2e`. Önceki inceleme `7dc5e56` üzerindeydi;
yeni değişiklikler henüz bu daldaki 98-test/ölçüm kanıtına dahil değil.
Bu değişiklikler 0.1.13 için incelendi ve PR dalına birleştirildi; Git
çatışmaları çözüldü. Aynı regresyon paketi eski 5494a2e kaynağındaki hataları
tekrar gösterdi; birleşik adayda geçti. Ana dala merge hâlâ ekip incelemesini bekler.

Son güncelleme: 10 Ekim 2026. Durumlar yalnız bu repodaki kanıta dayanır.
Son kod adayı **0.1.12**: Miraç'ın `7dc5e56` entegrasyonu incelendi ve
[bulunan hatalar düzeltildi](mirac-integration-review.md); 98 yerel test geçti.
0.1.10 yayımlandı, üç tekrarda 6/7 vaka geçti. Sonraki canlı düzeltme/ölçüm
[güncel raporda](live-validation.md) takip edilir. Aşağıdaki pilot ve ilk geniş
test sayıları tarihsel kayıttır; güncel skor yerine kullanılamaz.
Miraç'ın raporunda B public vakalarının kullanıldığı belirtiliyor; B artık ekip
genelinde kullanılmamış holdout sayılamaz. CLI split adı eski ayrımı koruyor.
İlk geniş test: 19 gerçek çağrı (önceki pilot hariç); başlangıçta 17'si birleşik scorer
ile puanlandı, son ikisinin ledger okuması servis 500/1101 hatasında engellendi.
Son iki çağrı daha sonra salt okunur kurtarmayla 1/2 puanlandı; eski engel kaydı korundu.
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
0.1.9 aynı workflow'un v10 sürümüydü; 0.1.10 v11, 0.1.11 v12 olarak doğrulandı.

| Sahip | İş | Durum / kabul ölçütü |
| --- | --- | --- |
| Kullanıcı | Brief + OpenAPI okuma, workflow üretimi (`builder/core.py`, `builder/calendar.py`) | Kimlik, şema, takvim ve gün ifadesi düzeltmeleri uygulandı; 0.1.12'nin canlı tekrarlı ölçümü bekleniyor. |
| Kullanıcı | Geliştirme vakalarından genel hata analizi ve otomatik düzeltme | Hatalar incelendi, birkaç aday karşılaştırıldı. Genel otomatik onarım motoru henüz yok; düzeltmeler asistan tarafından geliştirildi. |
| Arkadaş | Miraç Freya workspace'inde `builder/runtime.py` dağıtımını doğrulama | 0.1.10 v11 ve 0.1.11 v12 yayın/export/geri okuması tamamlandı. Anahtar-workspace kontrolü otomatik. |
| Arkadaş | `builder/evaluate.py` ile resmî public geliştirme vakalarını ölçme | 0.1.10 üç tekrar tamamlandı; 0.1.11 devam ediyor. Eski iki çağrı salt okuma kurtarmasıyla puanlandı. Tek test operatörü bu oturumdaki asistan. |
| Arkadaş | Hata/timeout ve sonuç kaydı | Araç hatası, uzakta hâlâ çalışan iş olasılığı ve hesaplanan/gerçek maliyet ayrı. Belirsiz toplam `null`. |
| Ortak | `builder/build.py`, sözleşme, bütçe, sürüm | Değişiklik için ilgili iki parça testi ve PR incelemesi. |
| Ortak | Public regresyon ve genelleme | B'nin üç vakası ekipçe kullanılmış; tekrarları regresyondur. Kalan A vakalarının ekip kullanım geçmişini doğrula; bağımsız genelleme ölçümü hâlâ yok. |
| Ortak | Temiz ortam, son commit, iki export + iz ve resmî teslim | `scripts/release.py`, `scripts/verify_release.py`; eksik final verileri tamamlanmadan teslim edildi sayılmaz. |

## Sıradaki çalışma sırası

11 Ekim güncellemesi: kritik kimlik/transfer/kayıt/bütçe düzeltmeleri 0.1.15'te
uygulandı, Miraç'ın 3d731be kaydı birleştirildi. 114 temiz ortam testi geçti.
Kullanıcı son canlı turu beş dakikaya indirdi; iki hedefli A vakasıyla
başlandı. Güncel durum [approved-quick-checks.md](approved-quick-checks.md).
Önceki bakiye ve sürüm bilgileri tarihsel kayıttır. Sıradaki öncelik yeni resmî
girdileri sözleşmeye göre işlemek; gizli değerlere göre kaynak kodu ayarlamamak.

1. İş bölümü PR'si açıldı; `mbirlik24` yazma erişimi doğrulandı. Her bilgisayarda ayrı klon/dal ve PR incelemesi.
2. API dağıtımı tamam. Kullanıcı bu oturumda test operatörü olarak asistanı seçti;
   arkadaş aynı anda simülasyon başlatmamalı. Banka anahtarı sabit ve yerel tutulmalı.
3. Eski tur salt okunur kurtarıldı. Güncel adayın yedi geliştirme vakasını ve
   üç tekrar tutarlılığını, ardından kalan public A ve B vakalarını ölç.
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
