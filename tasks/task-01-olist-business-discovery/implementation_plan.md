# 🎯 HVIA Internship — Task 1: Olist Business & Data Strategy

## 📌 نبذة عن المهمة والهدف العام
هذا التكليف التدريبي من شركة **HVIA – Data & AI Solutions** مصمم لتقييم مهارات البحث والتفكير التحليلي والربط بين الأرقام واستراتيجيات الأعمال، وتقديم مقترح احترافي كشريك حلول بيانات وذكاء اصطناعي لشركة **Olist** البرازيلية.

الشعار التوجيهي الأساسي للتاسك (صفحة 9):  
> **"Don't sell a tool. Find a problem worth solving."**

---

## 📋 هيكل التسليم الرسمي (Official Submission Requirements)

وفقاً لوثيقة التاسك الرسمية (صفحة 10 — **YOUR SUBMISSION**)، يتكون ملف التسليم الأساسي من **5 أركان رئيسية**:

| # | الركن الأساسي | المحتوى المطلوب في ملف التسليم |
|---|---------------|-------------------------------|
| 1 | **Company Research Summary** | ملخص مركز وشامل لفهم Olist، نموذج عملها، تحولها الاستراتيجي، وموقعها في السوق |
| 2 | **Dataset Understanding & Key Findings** | هيكل الـ **9 جداول**، العلاقات بينها، سلامة البيانات، وأهم الأرقام العامة |
| 3 | **Analysis & Business Story** | الغوص التحليلي في مشكلات وفرص البيزنس وربط الأرقام بالأثر المالي والتشغيلي |
| 4 | **Solution Proposal (What HVIA Could Offer)** | صياغة حلول واقعية تلائم Olist تحت مظلة مجالات HVIA الستة للبيانات والذكاء الاصطناعي |
| 5 | **Outreach Message Draft** | رسالة تواصل احترافية ومقنعة موجهة لصانع قرار في Olist |

### 📎 الملحقات والمهام التكميلية (Supporting & Professional Deliverables):
- **Supporting Work:** كود التحليل الكامل (Jupyter Notebook / Scripts) والرسوم البيانية المرجعية.
- **LinkedIn Milestone Post:** منشور احترافي على لينكد إن يوثق التجربة والتعلم من البيانات الحقيقية وتحديات ربطها بالبيزنس، مع الإشارة الرسمية لشركة **HVIA – Data & AI Solutions**.

---

## 🗂️ هيكل جداول البيانات (9 Relational Tables)

البيانات متوفرة ومجهزة محلياً في مجلد `../../archive/` وتتكون من **9 ملفات CSV مترابطة**:
1. `olist_orders_dataset.csv` (الجدول المحوري - 99,441 طلب وتواريخ المراحل)
2. `olist_customers_dataset.csv` (بيانات العملاء ومواقعهم وتتبع التكرار `customer_unique_id`)
3. `olist_order_items_dataset.csv` (تفاصيل السلة، الأسعار، وقيمة الشحن - 112,650 عنصر)
4. `olist_order_payments_dataset.csv` (طرق السداد، الأقساط، والقيم المدفوعة)
5. `olist_order_reviews_dataset.csv` (التقييمات من 1 إلى 5 والملاحظات النصية)
6. `olist_products_dataset.csv` (مواصفات المنتجات، الفئات، الأوزان، والأبعاد)
7. `olist_sellers_dataset.csv` (قاعدة البائعين ومواقعهم الجغرافية)
8. `olist_geolocation_dataset.csv` (إحداثيات الرموز البريدية البرازيلية)
9. `product_category_name_translation.csv` (ترجمة أسماء الفئات من البرتغالية للإنجليزية)

---

## 🏗️ مراحل التنفيذ خطوة بخطوة

```
[ المرحلة 1: التحضير والتأصيل ]
   └── مراجعة بحث الشركة (تم إنجاز olist_company_research.md وتدقيقه قانونياً وتاريخياً)

[ المرحلة 2: التحليل الاستكشافي المتعمق (In-Depth EDA) ]
   ├── إعداد وتشغيل Jupyter Notebook بالرسوم البيانية المتخصصة
   ├── فحص جودة البيانات (Missing values, Outliers, Delivery lead times)
   ├── تشخيص نقاط الاختناق:
   │    • تحليل الشحن والتأخير (Delivery Delays vs Customer Review Scores)
   │    • ولاء العملاء وتكرار الشراء (Repeat Purchase & Retention)
   │    • تركز أداء البائعين ومبيعات الفئات (Pareto 80/20 Distribution)
   │    • الأثر المالي للشحن (Freight-to-Price Ratios across States)
   └── استخلاص الـ Business Story المدعومة بالأدلة الإحصائية

[ المرحلة 3: هندسة حلول HVIA (Business-First AI Solutions) ]
   └── مطابقة المشكلات المستخرجة مع المجالات الستة لـ HVIA:
        1. Analytics & Decision Systems
        2. Automation & Data Pipelines
        3. Forecasting & Predictive Solutions
        4. Customer Intelligence
        5. Logistics Intelligence
        6. AI-Assisted Operations

[ المرحلة 4: صياغة المخرجات النهائية للتسليم ]
   ├── تجميع تقرير التسليم النهائي المتكامل الشامل للأركان الـ 5
   ├── إعداد مسودة رسالة الـ Outreach لصانع القرار في Olist
   ├── إعداد صيغة منشور الـ LinkedIn الاحترافي بما يبرز اسم وخبرة HVIA
   └── تنظيم ملفات المشروع وملف الـ Notebook ليكون قابلاً للمراجعة والتشغيل بسهولة
```

---

## 🎯 معايير الجودة والتحقق (Verification & Quality Standards)
- [x] تصحيح وتدقيق عدد الجداول إلى 9 جداول رسمية متطابقة مع وثيقة التاسك.
- [x] تدقيق الاسم القانوني لـ Olist إلى `Olist Serviços Digitais Ltda.` مع توثيق صفقة فينتك Flip وصندوق الـ FIDC.
- [x] اعتماد الأرقام الإحصائية المحسوبة برمجياً من ملفات الـ CSV الحقيقية.
- [x] ربط مقترحات الحلول بالمشكلات الفعلية المستخرجة من التحليل دون افتراض نماذج مسبقة.
- [ ] إخراج تقرير احترافي جاهز للتقديم يعكس عقلية استشاري حلول الذكاء الاصطناعي.
