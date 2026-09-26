"""
Arabic understanding PDF for HVIA Task 1 (not the official EN submission).
"""
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from fpdf import FPDF, XPos, YPos

OUT = Path(__file__).resolve().parent.parent / "outputs" / "HVIA_Task1_Arabic_Understanding.pdf"
CHARTS = Path(__file__).resolve().parent.parent / "outputs" / "charts"
FONT = r"C:\Windows\Fonts\arial.ttf"
FONT_B = r"C:\Windows\Fonts\arialbd.ttf"
OUT.parent.mkdir(parents=True, exist_ok=True)


def ar(text: str) -> str:
    """Shape + bidi for RTL Arabic display in fpdf."""
    if not text:
        return text
    # Keep digits/latin readable: reshape Arabic parts
    return get_display(arabic_reshaper.reshape(text))


class Doc(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.add_font("Ar", "", FONT)
        self.add_font("Ar", "B", FONT_B)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Ar", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(
            0, 5, ar("HVIA | فهم التاسك بالعربي | Olist (مش التسليم الرسمي)"),
            align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
        )
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("Ar", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"{self.page_no()}/{{nb}}", align="C")

    def h1(self, text):
        self.set_font("Ar", "B", 14)
        self.set_text_color(20, 40, 70)
        self.multi_cell(0, 7, ar(text), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def h2(self, text):
        self.ln(1.2)
        self.set_font("Ar", "B", 11)
        self.set_text_color(30, 60, 100)
        self.multi_cell(0, 6, ar(text), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.4)

    def body(self, text):
        self.set_font("Ar", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, ar(text), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    def bullet(self, text):
        self.set_font("Ar", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(
            0, 5.3, ar("• " + text), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )

    def figure(self, filename, caption, width=155):
        path = CHARTS / filename
        if not path.exists():
            self.body(f"[شارت ناقص: {filename}]")
            return
        need = width * 0.52 + 12
        if self.get_y() + need > self.page_break_trigger:
            self.add_page()
        x = self.l_margin + (self.epw - width) / 2
        self.image(str(path), x=x, w=width)
        self.ln(0.5)
        self.set_font("Ar", "", 8)
        self.set_text_color(80, 80, 80)
        self.multi_cell(
            0, 4, ar(caption), align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT
        )
        self.ln(1)


def build():
    pdf = Doc()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(14, 14, 14)

    # Cover
    pdf.add_page()
    pdf.set_fill_color(20, 40, 70)
    pdf.rect(0, 0, pdf.w, 36, style="F")
    pdf.set_y(10)
    pdf.set_font("Ar", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(
        0, 8, ar("نسخة عربية للفهم — تاسك HVIA"),
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_font("Ar", "", 11)
    pdf.multi_cell(
        0, 6, ar("Olist Business Discovery | بحث + داتا + مشاكل + حلول"),
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.set_y(42)
    pdf.set_text_color(50, 50, 50)
    pdf.set_font("Ar", "", 10)
    pdf.multi_cell(
        0, 5.5,
        ar(
            "الملف ده للشرح والفهم بالعربي. التسليم الرسمي لـ HVIA بالإنجليزي منفصل. "
            "الأرقام من تحليل ملفات archive الحقيقية."
        ),
        align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.ln(2)
    pdf.body("مسار القراءة: مين الشركة؟ ← إيه الداتا؟ ← إيه المشاكل؟ ← إيه حلول HVIA؟")

    # A
    pdf.h1("أ) بحث الشركة — Olist عبر الزمن")
    pdf.body(
        "Olist تساعد تجار SMB البرازيليين يبيعوا أكتر عبر التكنولوجيا. "
        "المؤسس: Tiago Dalvi | المقر: كوريتيبا | يونيكورن 1.5 مليار دولار (2021) | "
        "تمويل أكثر من 320 مليون | أكثر من 50 ألف تاجر."
    )
    pdf.h2("موديل فترة الداتا (2016–2018) — الأهم للتاسك")
    pdf.body(
        "تاجر ينضم لـ Olist ← المنتج يتباع تحت حساب/واجهة Olist الموحّد على الماركت بليس ← "
        "العميل يشتري من «Olist» ← التاجر يشحن. الإيراد: عمولة تقريبًا 19–21% + رسوم."
    )
    pdf.bullet("خطر الهوامش الضعيفة كوسيط")
    pdf.bullet("عدوى السمعة على الحساب الموحّد (بائع سيء يضر الكل)")
    pdf.bullet("خروج التجار لما يكبروا ويفتحوا حساب مباشر")
    pdf.h2("تايملاين مختصر")
    pdf.bullet("2007: Solidarium (قبل Olist)")
    pdf.bullet("2014–15: تأسيس Olist كجسر للماركت بليس")
    pdf.bullet("2016–18: نافذة الداتا — Olist Store / حساب موحّد")
    pdf.bullet("2019–20: Clickspace + PAX لوجستيات")
    pdf.bullet("2021: Tiny ERP + Vnda + يونيكورن")
    pdf.bullet("2022–24: تركيز SaaS")
    pdf.bullet("2025: Flip تمويل للتجار | 2026: إنهاء نموذج المتجر الموحّد تدريجيًا")
    pdf.body(
        "لاحقًا Commerce OS (ERP، Vnda، Pax، Flip…) = سياق بحث فقط. "
        "التحليل والحلول تحت موديل 2016–2018."
    )

    # B
    pdf.add_page()
    pdf.h1("ب) فهم الداتا")
    pdf.body(
        "استخراج عام لطلبات Olist Store تقريبًا من سبتمبر 2016 إلى أكتوبر 2018. "
        "حوالي 99.4 ألف طلب و9 جداول. مش موجودة: إعلانات، اشتراكات، SaaS بعد 2018."
    )
    pdf.h2("الجداول (باختصار)")
    pdf.bullet("orders (99,441): المحور — الحالة والتواريخ والـ ETA")
    pdf.bullet("order_items (112,650): سعر، شحن، منتج، بائع")
    pdf.bullet("customers: الولاء الحقيقي من customer_unique_id (96,096 شخص)")
    pdf.bullet("sellers (3,095) + products (~33 ألف) + payments + reviews")
    pdf.bullet("geolocation: متوسط إحداثيات لكل ZIP | ترجمة الفئات 71 صف")
    pdf.h2("قواعد مهمة قبل الأرقام")
    pdf.bullet("جمّع من مستوى العنصر لمستوى الطلب قبل حساب التأخير vs التقييم")
    pdf.bullet("نصوص المراجعات ناقصة كثير — تحليل النص عيّنة متحيزة")
    pdf.h2("لقطة أرقام")
    pdf.bullet("إيراد منتجات R$13.6M | متوسط الطلب ~R$138")
    pdf.bullet("تأخير عن ETA: 6.8% | تقييم في الوقت 4.29 vs متأخر 2.27")
    pdf.bullet("مشترٍ مرة واحدة: 96.9% | أعلى 10% بائعين ≈ 67.5% إيراد")
    pdf.bullet("SP: ~42% عملاء و~60% بائعين")

    # C
    pdf.add_page()
    pdf.h1("ج) المشاكل — قصة البيزنس من الداتا")
    pdf.body(
        "السلسلة: نمو سريع ← جغرافيا/شحن ← تأخير ← انهيار تقييم ← ولاء ضعيف، "
        "مع تركّز بائعين تحت وجه Olist واحد."
    )

    pdf.h2("1) التأخير يدمّر التقييم (أقوى مشكلة)")
    pdf.body(
        "6.8% بس متأخرين، لكن التقييم ينزل من 4.29 إلى 2.27 (−2.02 نجمة). "
        "في موديل الحساب الموحّد دي عدوى سمعة مش بس رضا عميل. "
        "تعليقات نجمة واحدة: التسليم/التأخير ~41% مقابل المنتج ~13%."
    )
    pdf.figure(
        "06_delivery_vs_review_scores.png",
        "شكل: التقييم عند الالتزام مقابل التأخير",
    )

    pdf.h2("2) ولاء شبه صفر")
    pdf.body(
        "96.9% يشتروا مرة واحدة فقط. النمو اكتساب مش تراكم قاعدة. "
        "تجربة سيئة في أول طلب (خصوصًا التأخير) تقتل فرصة الطلب التاني."
    )
    pdf.figure(
        "08_customer_retention_crisis.png",
        "شكل: أزمة تكرار الشراء",
    )

    pdf.h2("3) تركّز البائعين (Pareto)")
    pdf.body(
        "أعلى 10% ≈ 67.5% من إيراد المنتجات؛ أدنى 50% ≈ 3.2%. "
        "البائع الضعيف ممكن يضر السمعة حتى لو مبيعاته قليلة."
    )
    pdf.figure(
        "10_seller_pareto_curve.png",
        "شكل: منحنى Pareto للبائعين",
    )

    pdf.add_page()
    pdf.h2("4) فجوة جغرافية ومسافة")
    pdf.body(
        "نفس الولاية ~7.5 يوم مقابل بين الولايات ~14.7. "
        "وسيط المسافة ~434 كم وارتباطها بأيام التسليم ~0.39. وعد وطني واحد يواجه واقع غير متساوٍ."
    )
    pdf.figure(
        "16_distance_vs_delivery.png",
        "شكل: المسافة مقابل التسليم",
    )

    pdf.h2("5) ضغط الشحن + نمو موسمي (سياق)")
    pdf.bullet("الشحن ~17% من إيراد المنتجات؛ حصة الشحن من السعر+الشحن ~21%")
    pdf.bullet("ذروة نوفمبر 2017: 7,544 طلب — تضخّم مشاكل SLA وقت الضغط")
    pdf.body(
        "أولوية الحلول: (1) التأخير/التقييم (2) الولاء (3) صحة البائعين — "
        "ثم الجغرافيا والشحن كجذور داعمة."
    )

    # E
    pdf.add_page()
    pdf.h1("هـ) حلول HVIA المقترحة")
    pdf.body(
        "المبدأ: لا تبع أداة — لاقِ مشكلة تستحق الحل. "
        "كل حل مربوط بمشكلة من التحليل."
    )

    pdf.h2("خريطة سريعة")
    pdf.bullet("P1 ← نظام توقع مخاطر التأخير والاستجابة (أساسي)")
    pdf.bullet("P2 ← علم مخاطر عدم العودة بعد أول طلب (أساسي)")
    pdf.bullet("P3 ← درجة صحة البائع Seller Health Score (أساسي)")
    pdf.bullet("P4 ← ETA ديناميكي جغرافي (داعم لـ 1)")
    pdf.bullet("P5 ← تنبيه نسبة الشحن في الكتالوج (جانبي)")
    pdf.bullet("P6 ← فرز نص شكاوى التسليم (داعم لـ 1 و 2)")
    pdf.bullet("P7 ← إشارة الطلب الموسمي (داعم لـ 1)")

    pdf.h2("الحل 1 — توقع التأخير والاستجابة")
    pdf.body(
        "وقت تجهيز الشحن: نحسب احتمال فوات الـ ETA الموعود. "
        "خطر متوسط ← إخطار العميل بموعد واقعي قبل فوات الموعد. "
        "خطر عالي + بائع ضعيف ← تصعيد للتاجر ودعم أولوية. "
        "الهدف: تصغير فجوة التقييم (−2.02 حاليًا)."
    )

    pdf.h2("الحل 2 — علم الاحتفاظ بعد أول طلب")
    pdf.body(
        "بعد أول طلب مكتمل: نحدد مين يستاهل تواصل احتفاظ موجّه "
        "(مش حملة للكل)، باستخدام إشارة التأخير وصحة البائع وقيمة الطلب."
    )

    pdf.h2("الحل 3 — صحة البائع")
    pdf.body(
        "درجة من التأخير + التقييم + الإيراد + الاتجاه. "
        "شرائح: احمِ ونمِّ / راقب / يحتاج تدخل. "
        "تدخل في موديل التأخير وفي أولوية الدعم. "
        "يُفضّل بناؤه أولًا أو مع الحل 1."
    )

    pdf.h2("ترتيب البناء")
    pdf.bullet("أولًا: الحلول 1–3 (الأساسية)")
    pdf.bullet("ثم: ETA الجغرافي + إشارة الموسمية")
    pdf.bullet("ثم: فرز نص المراجعات")
    pdf.bullet("أخيرًا: تنبيه الشحن في الكتالوج")

    pdf.ln(2)
    pdf.body(
        "جملة العرض: HVIA تساعد Olist تحمي سمعة الحساب الموحّد واقتصاد العمولة "
        "بتوقع خطر التأخير قبل انهيار التقييم، وتركيز الاحتفاظ على أول طلبات متضررة، "
        "وترتيب البائعين حسب الصحة مش حسب الـ GMV بس."
    )

    pdf.ln(3)
    pdf.set_font("Ar", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0, 5,
        ar(
            "نهاية النسخة العربية للفهم. التسليم الإنجليزي: "
            "HVIA_Task1_Olist_Preview_A_B_C_E.pdf | المصدر التفصيلي: "
            "hvia_task1_arabic_understanding.md"
        ),
        align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )

    pdf.output(str(OUT))
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    build()
