# Freya belge arşivinin incelemesi

Kaynak dal: `docs/hackathon-kickoff-sync`, katkı commit'i `561a7cd`, yazar
`mbirlik24`. Bu katkı uygulama kodunu değiştirmiyor: kılavuz, transkript ve
genel platform belge kopyaları ekliyor. İnceleme dalına geçmişiyle alındı.

10 Ekim envanteri: `freya_docs/` altında **188 Markdown + 4 JSON** (192 dosya,
5.290.637 bayt). Dört JSON da ayrıştırılabiliyor; iki OpenAPI şeması iki farklı
yolda birebir kopya. Kopyalar katkı geçmişini korumak için silinmedi. Tek satırlı
kickoff transkripti zaman damgalarında paragraflara ayrıldı, otomatik transkript
ve güncel yazılı kurallar arasındaki kaynak önceliği açıklandı.

## Kaynak önceliği

1. Güncel organizatör açıklaması ve [yarışma kuralları](hackathon-rules.md).
2. Değiştirilmeden saklanan v3 `starter-v3/build-the-builder/docs/` ve `freya.py`;
   yarışma workflow üretimi ve scoring bu kaynağa dayanır.
3. [Genel Freya API arşivi](freya_docs/index.md); ilgili endpoint için referans.
   Genel platform özellikleri yarışmada otomatik olarak izinli sayılmaz.
4. [Ekip özeti](HACKATHON_GUIDE.md) ve [transkript](KICKOFF_TRANSCRIPT.md);
   eksiksiz veya hatasız resmî kural belgesi sayılmaz.

Özette düzeltildi: tek üretim zorunluluğu, her vaka için tek ödeme sözü varsayımı,
kanıtsız Owner rolü ifadesi ve yanlış doküman adedi. 30 dakika, modeller, teslim
saatleri ve sırları koruma şartları ana kurallar belgesinde bulunur.

## Entegrasyonda kullanılan ek belgeler

- [Simülasyon oluşturma](freya_docs/api-reference/simulations/create-simulation.md):
  belgeli `maxRetries=0`, `maxConcurrentCalls=1` ile tekrar ve eşzamanlı çağrı sınırı.
- [Simülasyon listesi](freya_docs/api-reference/simulations/list-simulations.md):
  yazmadan önce `status=running` ile workspace kontrolü.
- [Kredi bakiyesi](freya_docs/api-reference/workspace-credits/get-credits.md):
  deneme öncesi/sonrası kredi ve USD dönüşüm kaydı.

Bu kopyaların her satırı canlı platformda test edilmiş değildir. 5 MB genel
referans arşivi kaynak repoda kalır; çalıştırılabilir sürüm arşivine alınmaz.
Resmî yarışma kiti ve tekrar üretim için gerekli belgeler sürüme dahildir.
