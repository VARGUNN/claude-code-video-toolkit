# Dandik Haber · Seri kuralları

Instagram: @dandikhaber · 1080x1920, 60 fps, Reels

## Sabit karakter: Spiker Berkcan Dandikoğlu

Spiker serinin kilit karakteridir ve **hiçbir bölümde değişmez**: aynı yüz ve kıyafet (`SPIKER` nesnesi, 1. bölümden birebir kopyalanır, düzenlenmez), aynı ad (BERKCAN DANDİKOĞLU, Ana Haber Spikeri) ve aynı ses (ElevenLabs İmat Kaymaz, `hOVmUEz4hdueMxM4vipP`). Her bölüm stüdyoda onunla açılır ve onunla kapanır.

## Bölümler birbirine zincirlenir

1. **"Gelecek bölüm" yazısı yok.** Hiçbir videonun sonunda bitiş kartı, "gelecek bölüm" ya da "devamı yarın" gibi bir etiket olmaz.
2. **Her video bir cliffhanger ile biter.** Haber bitti sanılırken hikâyenin içinden yeni bir gelişme olur, video tam o anda kararır. İzleyici bunun cevabını bir sonraki videoda bulur.
3. **Her yeni video, önceki cliffhanger'ın devamıyla açılır (3-4 sn).** Spiker önceki haberin sonucunu tek cümleyle verir, sonra "Gelelim diğer haberimize..." ile o bölümün kendi haberine geçer.
4. **Takip çağrısı videonun içinde kalır.** Spiker "bizi takip etmeyi unutmayın" derken TAKİP ET · @dandikhaber butonu görünür. Bitiş kartı yoktur.

## Bölüm kaydı

| Bölüm | Kendi haberi | Açılış (önceki bölümün devamı) | Kapanış (cliffhanger) |
|---|---|---|---|
| 1 | Hayvanat bahçesinden kaçan aslan | Yok, ilk bölüm | Kafes yine boş. Parmaklıkta not: "VAPURDAYIM. MARTILARLA BİR HESABIM VAR. ASLAN" |
| 2 | Bursa'da giden kamyonetin motoruna yatan usta (gerçek olay, Mayıs 2026) | "Son dakika! Aslanımız Kadıköy vapurunda martılarla simit kavgasına tutuştu!" | Freni boşalan kamyonet stüdyoya geliyor. Spiker: "Bir dakika... Bu korna... bizim kapının önünden mi geliyor?!" KÜT, kararır. |
| 3 | Belirlenecek | Kamyonet stüdyonun ortasında, usta masanın altında motoru dinliyor | Belirlenecek |

Sesler: Muhabir Berk = Arman Kurt, Cemal Abi = Doğan Dağtaş, Recep Usta = Mehmet, Aslan = Onur Ozan.

## Teknik not

Bölümün kapanışı `src.html` içindeki `T.empty`, `T.drop`, `T.whip` ve `T.black` zamanlarıyla kurulur. Yeni bölümde açılış repliği `LINES` listesinin ilk elemanıdır ve en fazla 4 saniye sürer.
