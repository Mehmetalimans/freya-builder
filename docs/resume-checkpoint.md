# Ara verme kaydı — 10 Ekim 2026

**11 Ekim güncellemesi:** Kullanıcı son testlerin sürdürülmesini istedi.
Bu belgenin ara verme durumu tarihsel kayıttır. Bekleyen 0.1.11 turu salt
okunur kurtarıldı; güncel birleşim/iletişim adayı 0.1.13 ve son kontroller
[final-checks.md](final-checks.md) içinde izlenir.

Kullanıcı açıkça ara vermeyi ve son kayıtları istedi. **Yeni test veya yayın
başlatma; kullanıcı devam dediğinde önce aşağıdaki uzlaştırmayı yap.**

## Kod ve platform

- Dal: `fix/mirac-integration-review`; PR: [#6](https://github.com/Mehmetalimans/freya-builder/pull/6).
- Son davranış değişikliği: `dc33a5e6e50d1930b8ed242ae9deed8317aa3d97`, builder **0.1.12**.
  98 yerel test ve temiz Python 3.12.14 ortamı geçti; aynı commit'in
  [Linux CI çalışması](https://github.com/Mehmetalimans/freya-builder/actions/runs/38071570673) geçti.
- 0.1.12 henüz canlıda değil. A'da **0.1.11 / platform v12** yayımlanmış durumda.
  A workflow `82c69318-2c6a-43d3-9661-a93ea8b9b99d`,
  agent `7e5da178-7701-4c97-a394-b4c93c4dc953`.
- A 0.1.12 hash: `aa1063886bd2c4582072e3d8fee4bba91811ac7e3dac187e7ada8dd218ba69de`.
  B 0.1.12 hash: `a677ba9a97bea4aecb55858432a64b188b2ea47256ffebf0c7fa0d96710f73aa`.
- Miraç workspace: `8783bb12-56fc-489a-8608-590676971f6c`.
  Mevcut B workflow: `90a49196-df7c-4d06-bfbf-6668bc7fbeee`,
  agent `055dcb55-cc1f-49d7-80d4-05e2b6db286e`.
  B'nin mevcut tanımı yerel `runs/live-0110-preflight/prior-b-workflow.private.json`
  dosyasına yedeklendi. `state/84063c2bdbd5abb8.json` henüz yalnız A slotunu içerir;
  B'yi tekrar kullanmadan önce bu eşleşmeyi doğrula. Yeni workflow çoğaltma.

## Ölçümler ve kesilen tur

- 0.1.10: `runs/20261010T165121Z-a6ff9daf`; 7/7, 6/7, 6/7;
  19/21 çağrı ve tüm tekrarlar hesabıyla 6/7 vaka. Tam resmî sonuç kayıtlı.
- 0.1.11: `runs/20261010T171642Z-f10bfb65`; ilk iki tur **6/7 ve 7/7**.
  Üçüncü tur sırasında kullanıcı ara istedi; yerel worker durduruldu.
  `repetition-01.json`, `repetition-02.json`, izler ve export korunuyor.
  Tamamlanmış üç tekrar skoru **yok**; iki turun oranını üç tekrar skoru sayma.
- Son simülasyon `c1ede396-81e9-45d7-ba6d-35462871c6e5`,
  iteration `231bcbe8-fd03-4ff2-94ef-a47ca8cb803f`.
  Belgeli PUT ile `paused` istendi ve ilk geri okumada doğrulandı; sonraki
  okumada sunucu yeniden `running` gösterdi. Bu API durum güncellemesinin
  başlayan çağrıları iptal ettiği varsayılamaz. Güncel son gözlem
  [`reports/live-pause.json`](../reports/live-pause.json) içinde.
  Son kontrolde uzak simülasyon **completed**, yedi uzak judge sonucu **pass**;
  çalışan/kuyruktaki çağrı kalmadı. Bu, banka ledger'ıyla birleşik scorer yerine
  kullanılamaz; üçüncü turun birleşik puanlaması ve rezerv uzlaştırması bekliyor.
- `state/budget-ledger.json` bekleyen koşuyu korur. **Rezervi körlemesine
  silme ve simülasyonu yeniden oluşturma.** Önce uzak işin gerçek durumunu,
  tamamlanan çağrıların banka ledger'ını ve faturalamayı salt okunur kontrol et.
  `builder/recover.py` mevcut haliyle tek-tekrar kurtarması için yazılmıştır;
  üç tekrarlı kesilen koşuya doğrudan çalıştırıp eksik skoru geçerli sayma.
  Gerekirse eksik turun resmî scorer'la salt okunur kurtarılmasını ayrıca uygula.

## Devam sırası ve sınırlar

Sonraki dil/Git kontrolünde resmî İngilizce ve metin şartı yeniden doğrulandı.
Mevcut prompt ve simülasyon modu buna uygun; davranış hash'leri değişmedi.
Uzak `integration/v3-final`, `5494a2ee7de304351ce7802550aa9b287d0d5c16`
commit'ine ilerledi (`1aefb49`, `803203f`, `5494a2e`). Bu üç commit önceki
Miraç incelemesinin kapsamında değildi. PR birleştirmeden veya yeni ortak
aday belirlemeden önce bunları incele; bu dalın test sonuçlarını onlara atfetme.

1. API anahtarını yalnız güvenli yerel süreç ortamından yükle; sohbete/repoya yazma.
   Banka takım anahtarı mevcut yerel `state/browser-bank-team-key` dosyasındadır;
   yeni anahtar oluşturma. Ekip adına tek simülasyon operatörü bu asistandır.
2. Bekleyen 0.1.11 turunu uzlaştır; gerçek sonuç ve tüketim kaydıyla rezervi kapat.
3. 0.1.12'yi aynı A slotuna yayımla/export/geri oku. A geliştirme 7 vaka × 3;
   ardından sabit hash ile kalan A 3 vaka × 3 ve B 3 vaka × 3.
   İç testlerle birlikte brief başına 30 dakika sınırını açıkça izle;
   ayrı komutlar süre bütçesini sıfırlamış sayılmaz.
4. B ekipçe daha önce kullanıldı: regresyon kümesidir. Kalan A'nın ekip kullanım
   geçmişi doğrulanmadı. Gizli final başarısı veya bağımsız genelleme iddiası yok.
5. Sonuç raporu, README/tasks, temiz paket ve PR açıklamasını tamamla.
   Ana dala doğrudan push/merge yapma; Miraç'ın PR incelemesi gerekiyor.

Harcamaya izin **toplam 100 USD, yalnız Freya**; dış model çağrısı yok.
Workspace'e eklenen kredi izin artışı değildir. Kümülatif tüketimle 20 USD
tampon korunur; 80 USD gözlenen toplam tüketimde yeni test durur.
Yerel kota 26 simülasyon/120 vaka koşusu; planlanan son toplam 108 vaka koşusu.
Kesin fatura bilinmiyor. Genel otomatik onarım motoru ve final teslimi tamamlanmadı.
