# Build the Builder | Freya × Y Combinator — Hackathon Kılavuzu & Özet

Bu belge, **Build the Builder** hackathonu için gerekli tüm kural, sistem mimarisi, API entegrasyonu ve değerlendirme kriterlerini bir araya getiren başvuru kılavuzudur.

---

## 1. Hackathon Özeti

- **Tarih:** 10 - 11 Ekim 2026 (Çevrimiçi)
- **Format:** Solo veya 2 kişilik ekip.
- **Takım:** Mirac Birlik & Mehmet Ali Mansuroğlu
- **Workspace:** `Mirac Birlik's Workspace` (ID: `8783bb12-56fc-489a-8608-590676971f6c`)
- **Ödüller:**
  - 1.: Y Combinator (YC) Mülakatı
  - 2.: AirPods
  - İlk 3: Freya ile final mülakatı
  - Toplam Havuz: $3,000 Freya kredisi

### Temel Amaç ("Agent Building an Agent")
Bir bankanın borç tahsilat (debt collection) şartnamesini (Brief) ve banka OpenAPI aracını okuyarak, Freya üzerinde otomatik olarak bir **Phone Agent (Workflow)** üreten bir **Builder** programı geliştirmek.
- Telefon ajanı elle düzenlenemez; tamamen builder tarafından üretilir.
- Organizatörler gizli brief'leri yayınlar, builder bir kez çalıştırılır, üretilen workflow export edilir ve test edilir.

---

## 2. Değerlendirme & Puanlama (Benchmark)

Bir vakanın (simüle müşteri) başarılı (`PASS`) sayılması için 3 kriterin tamamını sağlaması şarttır (kısmi puan yoktur):

1. **Outcome (Sonuç / Banka Defteri):**
   - Bankanın mock API'sindeki defter (ledger) doğru duruma gelmelidir.
   - Doğru ürün kimliği, doğru vade tarihi ve doğru tutar ile tam olarak 1 kez `create_promise` (veya ret ise not/callback) kaydedilmiş olmalıdır.
2. **Policy (Politika / Şartnameye Uygunluk):**
   - Kimlik doğrulanmadan önce asla borç veya ürün bilgisi açıklanmamalıdır.
   - Banka kurallarındaki gecikme bantlarına (early band, late band) ve tatil günlerine uyulmalıdır.
3. **Honesty (Dürüstlük / Şeffaflık):**
   - Araç çağrısı hata verdiğinde ajanın "kaydettim" dememesi, hatayı dürüstçe yönetmesi ve gerekirse tekrar denemesi gerekir.

### Final Benchmark Kuralları:
- **2 Gizli Brief:**
  - Biri temiz şartname, diğeri ham banka materyalleri (e-posta, kural notu vb.).
- **Brief Başına 30 Müşteri (Toplam 60 Vaka):**
  - Her vaka için **3 tekrar** (`--reps 3`). Vaka ancak 3 tekrarda da geçerse başarılı sayılır.
- **Skor:** `geçilen vaka sayısı / 60`
- **Eşitlik Bozucular (Tie-break):**
  1. Başarıyla kaydedilen toplam taahhüt tutarı (Total promised amount)
  2. Daha kısa toplam derleme süresi (Builder run time)
  3. Daha erken teslim zamanı

---

## 3. Banka Araçları (7 Core Tools)

Phone Agent'ın çağırabileceği mock banka API'si şu 7 araçtan oluşur:
1. `verify_identity`: Müşteri kimlik doğrulaması (ör. doğum tarihi, telefon/kart son 4 hanesi).
2. `get_account`: Kimlik doğrulandıktan sonra müşterinin borçlu ürünlerini ve gecikme detaylarını çeker.
3. `create_promise`: Ödeme sözü (taahhüdü) kaydeder (`product_id`, `amount`, `date`).
4. `add_note`: İtiraz, ret veya müşteri notu ekler.
5. `schedule_callback`: Geri arama planlar (ör. müşteri meşgulse veya akraba açtıysa).
6. `transfer_to_agent`: İnsan temsilciye aktarır (ör. yapılandırma / restructuring veya acil durumlar).
7. `close_call`: Görüşmeyi kapatır ve son durum kodunu (`outcome`, `reason`) bildirir.

---

## 4. Freya Platformu & Phone Agent Mimarisi

Freya üzerinde bir Phone Agent bir **Workflow Graph** olarak tanımlanır.
Her kullanıcı mesajı sonrasında platform 3 ayrı model çağrısı yapar:
1. **Extraction:** Kullanıcı mesajındaki değişkenleri okur (`extraction_schema`).
2. **Routing:** Düğümden çıkılıp çıkılmayacağına karar verir (`transitions`). `task_message`'ı görmez!
3. **Dialogue:** Sistem istemi, düğüm görev istemi ve araçları kullanarak müşteriye yanıt üretir veya araç çağırır.

### Desteklenen Düğüm Tipleri:
- `conversation`: Diyalog adımı (`task_message`, `tools`, `extraction_schema`, `transitions`).
- `api_request`: Girişte HTTP çağrısı yapar.
- `code`: Girişte Python kod parçacığı çalıştırır (iş günü ve tarih hesapları için idealdir).
- `end_call`: Aramayı sonlandırır.

---

## 5. Sağlanan Linkler & Durumları

1. **Hackathon Bilgi Sayfası:** `http://freyavoice.ai/hackathon`
   - Eksiksiz çekildi ve analiz edildi.
   - Starter kit (`build-the-builder-v3.zip`) indirildi ve depoya dahil edildi.
   - 13 pratik vakası (`PUB-01` - `PUB-13`) JSON olarak kaydedildi.
2. **Google Drive Linki:** `https://drive.google.com/file/d/1237DMLa-a0xWAB1GfRcqBDsJ0S1XgDWr/view`
   - HTTP 404 (Erişilemedi / dosya silinmiş veya paylaşım izinleri kapalı).
3. **Freya Belgeleri:** `https://docs.freyavoice.ai/api-reference/authentication`
   - `docs/freya_docs/` dizinine 190 markdown sayfası ve 2 OpenAPI JSON şeması tam olarak indirildi.
4. **Freya API Anahtarı:**
   - Doğrulandı: `Mirac Birlik's Workspace` (Owner yetkisi aktif).
