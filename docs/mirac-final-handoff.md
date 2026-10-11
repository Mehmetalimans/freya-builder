# Miraç: final çalışma devri

Son teslim 11 Ekim 2026 23:00 İstanbul. Kullanıcı kalan çalışmayı Miraç'a devretti. Devir 21:15 İstanbul itibarıyla tamamlandı. **Final workflow henüz üretilip yayımlanmadı; final konuşma testi yapılmadı.** Mock 617/617, temiz Python ortamı 127/127 geçti. Üç üretim denemesi ve tam izleri `reports/final-generation-attempts.json` ile `reports/final-attempt-traces/` içinde. Son deneme 12 dakika çıktı vermeyince devir için durduruldu. Hiçbir final API yayını gerçekleşmedi.

**İlk görev:** genel üretim aşamasının fazla uzun yanıt üretmesini veya beklemesini teşhis et. Gereksinim özetini ve workflow büyüklüğünü genel olarak sınırla; vaka bilgisi sabitleme. Önce kısa bir kayıtlı üretim denemesini tamamla. Başarıda doğrulama/yayın/export/geri okuma ardından `scripts/final_evaluate.py` ile EX-1, sonra kalan beş resmî örneği birer kez ölç. Engellenen/iptal edilen üretimleri final başarı sayma.

Kaynak sürümü 0.2.1. Sürekli açık yerel operatörde paket sürümü önbellekte 0.2.0 kaldığından eski sonuç metadata’sı 0.2.0 yazabilir; davranışı belirleyen gerçek kaynak commit/hash kayıtları korunmuştur. Yeni üretimi temiz süreçte çalıştır. Seçilen final için yeni tam trace kullan.

## Önce açılacaklar

- Dal: `final/case-folder-builder`, taslak PR: https://github.com/Mehmetalimans/freya-builder/pull/7
- Girdiler: `cases/final/` — orijinal belgeler, sentetik müşteri cevapları, altı örnek senaryo. Salt okunur kabul et.
- Genel builder: `builder/case_folder.py`; CLI: `python builder/build.py {case_folder} {mock_url}`.
- Mock: `bank-mock/`; adres https://freya-final-bank.freya-final-bank-mock.workers.dev
- Kanıt: `reports/final-mock-contract.json` (617/617), `reports/final-generation-attempts.json` (başarısız denemeler), `docs/final-peer-review.md`.

## Çalıştırma

```console
git fetch origin
git switch final/case-folder-builder
git pull --ff-only
python -m pip install -r requirements-final.txt
npm ci --prefix bank-mock
python -m unittest discover -s tests -q
node bank-mock/export-fixtures.js state/mock-fixtures.json
python scripts/check_mock.py cases/final https://freya-final-bank.freya-final-bank-mock.workers.dev --fixtures state/mock-fixtures.json
python builder/build.py cases/final https://freya-final-bank.freya-final-bank-mock.workers.dev
```

Freya anahtarını yalnız yerel süreç ortamına koy. Workspace: `8783bb12-56fc-489a-8608-590676971f6c`. Codex CLI mevcut ChatGPT oturumuyla giriş yapmış olmalı; dış model API anahtarı kullanma. Builder varsayılan olarak yayınlar; yalnız üretim için `--offline`.

Bu bilgisayarda sistem DNS'inin verdiği 188.114.96.3/97.3 adreslerine bağlantı zaman aşımı oldu. Cloudflare'ın 1.1.1.1 resolver'ından gelen 104.21.80.118 ile aynı hostname/SNI ve normal TLS doğrulaması korunarak 617/617 test geçti. Kendi bilgisayarında önce normal DNS ile dene. Gerekiyorsa aynı doğrulama `bank-mock/check-remote.js` üzerinden yapılabilir; son parametre o anda DNS'ten doğruladığın IP'dir. Eski IP'yi kalıcı ağ ayarı olarak kullanma.

## Devam kuralları

- Tek workspace'te tek simülasyon. İlerlemeden önce açık işi kontrol et; timeout sonrasında uzaktaki durumu uzlaştır.
- Üretilmiş workflow ve export'u elle değiştirme. Genel builder hatasını düzelt, yeniden üret ve yeni tam oturum izini sakla.
- Final kurallarını builder kaynağına sabitleme. Dil, müşteri kimliği, tarih ve iş kuralları girdiden; hesap gerçekleri yalnız mock'tan gelir.
- Bankada yıllık hak ön-kontrolü ve fiziksel IVR yönlendirme sözleşmesi eksik. Bunları doğrulanmış platform özelliği gibi sunma. Prototip belgeli servis cevabını ve terminal niyetini kullanır; eksikler kayıtlı sınırlamadır.
- Eski practice OpenAPI'ye geri dönme. Eski İngilizce tahsilat veya iki-workflow teslim şemasını kullanma.
- Mock sonuçlar açıklanana kadar çalışır kalmalı. Henüz yayımlanmış adresi değiştirme veya servisi kaldırma.
- PR'nin tabanı integration/v3-final; olası çatışma incelemesi gerekir. Main'e doğrudan push veya izinsiz merge yapma.

## Teslimi tamamlama

Son Drive, e-posta ve resmî sayfa kontrolünü yap. Seçilen üretimin kendi resmî export'u ve tam `codex.session.jsonl` izi gereklidir. `scripts/final_submission.py prepare` dosyaları hazırlayıp kaynakla beraber commit'e alır; sonra `manifest` aynı commit'teki byte'ları doğrular. Submission alanları: team, members, repo, commit, run_command, workflow, trace, mock_url. Manifest metadata'sını ayrı commit'e alarak kendi SHA döngüsüne girme.

Üyeler: Mehmet Ali Mansuroğlu (mmansuroglu24@ku.edu.tr), Miraç Birlik (mbirlik24@ku.edu.tr). Takım etiketini Mehmet'le doğrula. `submission.json`, workflow ve tam izi yavuz@freyavoice.ai adresine göndermeden önce **Mehmet'ten açık gönderim onayı al**. Bu oturum henüz teslim e-postası göndermedi.
