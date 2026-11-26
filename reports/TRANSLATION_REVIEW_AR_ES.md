# Native Reviewer Sheet — Arabic (`ar`) & Spanish (`es`)

> **Status**: `DRAFT` — prepared for native reader sign-off (`CHECKPOINT 2.5 REVIEW`, Fix #4).
> Keep terms calm, plain-language, non-alarmist, and free of cybersecurity/intrusion connotations.

---

## PART A: ARABIC REVIEW SHEET (`ar.ts` + `wishes.json`)

### 1. Three Candidate Terms for `"breakthrough"`
Note: `"اختراق"` is intentionally avoided because in contemporary Arabic tech journalism it reads primarily as cyber-intrusion/breach (`hacking`), not a gift/discovery humanity asks for.

| # | Candidate Term | Literary / Nuance | Example Sentence (Headline / CTA Context) | Status |
|---|---|---|---|---|
| 1 | **`إنجاز` / `إنجازات`** *(achievement / milestone breakthrough)* | Familiar, calm, dignified; works naturally in singular and plural with everyday readers and policy researchers. | **جاهزية البشرية: هل نحن مستعدون لما نطلب من الذكاء الفائق تحقيقه؟ تخيل أن ذكاءً فائقاً يستطيع أن يقدم إنجازاً واحداً للبشرية.** *(CTA: `اختر إنجازاً`)* | **Current choice** |
| 2 | **`نقلة نوعية` / `نقلات نوعية`** *(qualitative leap)* | Emphasizes structural transformation / leap forward beyond ordinary tools; slightly longer in compact button labels. | **تخيل أن ذكاءً فائقاً يستطيع تحقيق نقلة نوعية واحدة للبشرية. اخترها، وشاهد وصولها، ثم انظر ما يتطلبه استقبالها.** *(CTA: `اختر نقلة نوعية`)* | **Alternative A (Leap)** |
| 3 | **`فتح علمي` / `كشف علمي` (أو `طفرة علمية` / `طفرات`)** *(discovery / scientific breakthrough leap)* | `طفرة` connotes a sudden leap forward; `كشف` emphasizes scientific discovery — warm for Open Problems, slightly narrower for Public Good (`نظّف نهري`). | **كل طفرة عظيمة تحتاج عالماً مستعداً. / كل كشف عظيم يحتاج عالماً مستعداً لاستقباله.** *(CTA: `اختر طفرة` / `اختر كشفاً`)* | **Alternative B (Discovery / Leap)** |

### 2. Fixed Arabic Copy for `"What the world is asking for"` (`ar.ts::wishWall`)
Removed the earlier loose phrasing `"الخريطة المشتركة العالمية"` (`shared global map`) to avoid confusion with Shadow Map:
- `wishWall.heading`: **`ما الذي يطلبه العالم؟`**
- `wishWall.emptyHeadline`: **`تُفتح صفحة «ما الذي يطلبه العالم؟» بعد أول 20 مساهمة مجهولة الهوية.`**
- `wishWall.emptyBody`: **`يبقى كل اختيار خاصاً في متصفحك تلقائياً. لا تظهر المواضيع الجماعية إلا عندما يختار 20 شخصاً حقيقياً على الأقل المساهمة.`**
- `wishWall.cta`: **`اختر إنجازاً`**

### 3. Every Arabic String — `Meet Toto` Card (`ar.ts::totoCard` + Hero caption)

| Key | English Reference | Current Arabic String | Notes / Review Question |
|---|---|---|---|
| `hero.totoCaption` | Toto arrives at dawn: "I can deliver one breakthrough per person. Ask clearly." | `يصل «توتو» عند الفجر: «أستطيع تقديم إنجاز واحد لكل شخص. اطلب بوضوح.»` | Phonetic `توتو` |
| `totoCard.eyebrow` | MEET YOUR GUIDE | `تعرّف على دليلك` | Check gender neutrality / warmth |
| `totoCard.heading` | Meet Toto. | `تعرّف على توتو.` | Natural intro |
| `totoCard.body` | Toto is a fictional superintelligence we use to explore one question: what happens when humanity gets exactly what it asks for? Toto is helpful, fast, and very literal. It delivers what you ask, not always what you meant. Together you'll test each breakthrough and see how ready the world is to receive it. | `توتو ذكاء فائق متخيل نستخدمه لاستكشاف سؤال واحد: ماذا يحدث عندما تحصل البشرية على ما تطلبه بالضبط؟ توتو متعاون وسريع وحرفي جداً؛ ينفذ ما تطلبه لا ما تقصده دائماً. ستختبران معاً مدى جاهزية العالم للاستقبال.` | Note dual verb `ستختبران` ("the two of you — you & Toto — will test") |
| `totoCard.chipsLabel` | What Toto is and is not | `ما هو توتو وما ليس عليه` | ARIA group label |
| `totoCard.chips[0]` | Fictional, not a real system | `شخصية خيالية، لا نظاماً حقيقياً` | Accusative predicate naturalness |
| `totoCard.chips[1]` | Helpful, never hostile | `متعاون، ولا يعادي أحداً` | Calm non-hostile phrasing |
| `totoCard.chips[2]` | Literal by design | `حرفيّ بالتصميم` | Or `حرفيّ بطبعه`? Flagged for preference |
| `totoCard.ctaPrimary` | Choose a breakthrough | `اختر إنجازاً` | Button text |
| `totoCard.ctaSecondary` | Read Toto's story | `اقرأ قصة توتو` | Link to `/toto/` |
| `totoCard.footnote` | Toto is a storytelling device. It is not a forecast and does not represent any real AI system. | `توتو أداة سردية متخيلة، وليس توقعاً مستقبلياً ولا يمثل أي نظام ذكاء اصطناعي حقيقي.` | Explicit disclaimer |
| `totoCard.svgAlt` | Toto, a fictional superintelligence depicted as a soft glowing dawn orb inside a thin ring | `توتو، ذكاء فائق متخيل مرسوم كجرم مضيء دافئ عند الفجر داخل حلقة رفيعة` | Image alt text |

### 4. Every Arabic String — `/toto/` Story Page (`ar.ts::totoPage`)

| Key | English Reference | Current Arabic String | Notes |
|---|---|---|---|
| `totoPage.eyebrow` | STORYTELLING GUIDE · FICTION | `دليل القصة · شخصية خيالية` | Badge pill |
| `totoPage.title` | Meet Toto. | `تعرّف على توتو.` | H1 |
| `totoPage.lead` | A fictional superintelligence used as a calm lens for exploring one question: what happens when humanity gets exactly what it asks for? | `ذكاء فائق متخيل نستخدمه كعدسة هادئة لسؤال واحد: ماذا يحدث عندما تحصل البشرية على ما تطلبه بالضبط؟` | Lead subtitle |
| `totoPage.posesLabel` | Toto visual poses | `حالات توتو البصرية` | Region aria-label |
| `totoPage.poses[0]` | Calm — When a breakthrough arrives cleanly and people are ready to steer it. | `هادئ — عندما يصل الإنجاز بسلاسة ويكون الناس مستعدين لتوجيهه.` | Alt: `توتو في وضعية هادئة: جرم دافئ متوازن داخل حلقة مستقرة` |
| `totoPage.poses[1]` | Curious — Asking the open question: "How would we know this worked?" | `فضولي — حين يطرح السؤال المفتوح: «كيف سنعرف أن هذا نجح؟»` | Alt: `توتو في وضعية فضولية: حلقة مدارية مائلة ونظرة متسائلة` |
| `totoPage.poses[2]` | Apologetic — Used in the Wobble when a literal delivery misses unstated context. | `معتذر — في لحظة الاهتزاز، عندما يكشف التنفيذ الحرفي عن سياق منسي.` | Alt: `توتو في وضعية اعتذار: وهج كهرماني لطيف يشير إلى مفارقة غير متوقعة` |
| `totoPage.whoTitle` | Who Toto is | `من هو توتو` | Card 1 title |
| `totoPage.whoBody` | A small name for a very large intelligence. The contrast is the point... | `اسم صغير لذكاء بالغ الاتساع؛ وهذا التباين مقصود. توتو متعاون وسريع وهادئ وفضولي وحرفي جداً: ينفذ ما يُطلب منه حرفياً لا ما يُقصد ضمناً.` | Card 1 body |
| `totoPage.rulesTitle` | Toto's three rules | `قواعد توتو الثلاث` | Card 2 title |
| `totoPage.rules[0]` | It delivers one breakthrough per person, then always shows the cost afterwards. | `يقدم إنجازاً واحداً لكل شخص، ثم يُظهر الكلفة والآثار الجانبية بعد ذلك دائماً.` | Rule 1 |
| `totoPage.rules[1]` | It never lies — and it never hides tradeoffs behind comfort. | `لا يكذب أبداً — ولا يخفي التحديات خلف وعود مريحة.` | Rule 2 |
| `totoPage.rules[2]` | It always asks: "How would we know this worked?" | `يسأل دائماً: «كيف سنعرف أن هذا عمل بشكل صحيح؟»` | Rule 3 |
| `totoPage.notTitle` | What Toto is not | `ما ليس عليه توتو` | Card 3 title |
| `totoPage.notBody` | Toto is not a forecast, not a real AI system or product, and never a villain... | `توتو ليس تنبؤاً ولا نظاماً حقيقياً أو منتجاً قائماً، وليس شريراً أبداً. إنه أداة سردية متخيلة تهدف إلى ربط الوعي بقدرة الإنسان على الفعل.` | Card 3 body |
| `totoPage.backCta` | Choose a breakthrough | `اختر إنجازاً` | Primary CTA |
| `totoPage.homeLink` | Back to homepage | `العودة للرئيسية` | Secondary link |

---

## PART B: SPANISH REVIEW SHEET (`es.ts`, short list)

### 1. Candidate Terms for `"breakthrough"`
- **Current choice (`avance` / `avances`)**: *«Imagina que una superinteligencia pudiera entregar un gran avance a la humanidad. Elige un avance.»*
- **Alternative A (`salto` / `gran salto`)**: *«Elige un gran salto»* (connotes leap cleanly, slightly informal for policy research).
- **Alternative B (`logro` / `hallazgo`)**: *«Todo gran logro necesita un mundo preparado»* (`logro` = achievement; `hallazgo` = discovery — `avance` bridges scientific discovery and civic gift best).

### 2. Spanish Strings for `Meet Toto` Card & `/toto/`
- **Meet Toto card (`totoCard`)**: `CONOCE A TU GUÍA` | `Conoce a Toto.` | Body: *«Toto es una superinteligencia ficticia que usamos para explorar una pregunta: ¿qué ocurre cuando la humanidad recibe exactamente lo que pide? Toto es servicial, veloz y muy literal: entrega lo que pides, no siempre lo que querías decir. Juntos pondrán a prueba cada avance.»* | Chips: `Ficción, no un sistema real`, `Servicial, nunca hostil`, `Literal por diseño` | Buttons: `Elige un avance`, `Leer la historia de Toto` | Footnote: `Toto es un recurso narrativo. No es un pronóstico ni representa a ningún sistema de IA real.`
- **`/toto/` page (`totoPage`)**: `GUÍA NARRATIVO · FICCIÓN` | `Conoce a Toto.` | Poses: `Sereno`, `Curioso`, `Disculpándose` | Sections: `Quién es Toto`, `Las tres reglas de Toto` (`Entrega un avance por persona y siempre muestra el costo después.`, `Nunca miente ni oculta consecuencias tras promesas cómodas.`, `Siempre pregunta: «¿Cómo sabríamos que esto funcionó?»`), `Qué no es Toto` (`Toto no es una predicción, ni un sistema real ni un villano...`).
- **Fixed `wishWall.emptyHeadline`**: *«Este espacio de «Lo que el mundo está pidiendo» abrirá tras los primeros 20 aportes anónimos compartidos.»*
