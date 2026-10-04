# LEADERS AI — مستقل عن Floot

## تشغيل محلي
1. Python 3.11+
2. `pip install -r requirements.txt`
3. انسخ `.env.example` إلى `.env`
4. ضع مفتاح OpenAI في `OPENAI_API_KEY`
5. شغّل:
   `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. افتح `http://127.0.0.1:8000`
7. لوحة الإدارة: `http://127.0.0.1:8000/admin`

## رفع مادة
من لوحة الإدارة سجّل بكلمة السر الموجودة في `.env` ثم ارفع PDF.
الموقع:
- يفهرس صفحات PDF.
- يرفع الملف إلى OpenAI File Search.
- يبحث عن الصفحات المرتبطة بالسؤال.
- يطلب من النموذج شرح المعلومة بدل نسخها.
- يعرض رقم الصفحة وصورة الصفحة الأقرب.

## النشر
يوجد Dockerfile وrender.yaml كنقطة بداية للنشر على Render.
للاستخدام الحقيقي مع عدد طلاب كبير يُفضّل PostgreSQL وتخزين ملفات دائم بدل SQLite/local disk.
