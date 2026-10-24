# قواعد الشغل على المستودع (Team Loader Store)

## أول مرة (القائد فقط)
```
cd loader-store
git init
git add .
git commit -m "SCRUM-0 initial project import"
git branch -M main
git remote add origin https://github.com/<ORG-OR-USER>/loader-store.git
git push -u origin main
```
بعدها من GitHub: Settings → Collaborators (ادعُ الـ 9 الباقيين) و Settings → Branches → Add rule على `main`: **Require a pull request before merging** + **Require 1 approval**.

## أول مرة (كل عضو)
```
git clone https://github.com/<ORG-OR-USER>/loader-store.git
cd loader-store
python server.py        # أو run-desktop.bat على ويندوز
```

## دورة الشغل لأي مهمة
1. خد آخر نسخة: `git checkout main && git pull`
2. افتح فرع باسم رقم المهمة: `git checkout -b SCRUM-104-add-part-api`
3. اشتغل، وكل شوية: `git add .` ثم `git commit -m "SCRUM-104 add POST /products validation"`
4. ارفع الفرع: `git push -u origin SCRUM-104-add-part-api`
5. على GitHub افتح **Pull Request** عنوانه `SCRUM-104 Add spare part API` وحدد المراجِع.
6. المراجِع يقرأ الكود ويجرّبه، ولو تمام يعمل Approve ثم Merge. ممنوع تدمج شغلك بنفسك.

## قواعد
- **رقم المهمة (SCRUM-xxx) لازم يكون في اسم الفرع وفي كل Commit وفي عنوان الـ PR** عشان Jira يربطهم.
- ممنوع الرفع المباشر على `main`.
- ممنوع تعمل Commit لملفات `data/` أو قاعدة البيانات أو كلمات مرور.
- Commit صغير ورسالته بتقول إيه اللي اتغير، مش «update» ولا «fix».
- لو اتعارض ملف (conflict): كلّم زميلك اللي عدّل نفس الملف، وماتمسحش شغله.

## مراجعة الكود (مين يراجع مين)
Frontend يراجعوا بعض، Backend يراجعوا بعض، وشغل القائد يراجعه Frontend 1.
المراجِع يسأل: هل بيشتغل؟ هل فيه قيمة بتتحط من غير تحقق؟ هل الصلاحيات متراعية؟ هل أنا فاهم الكود؟

## ملاحظة أمانة أكاديمية
جزء من الكود المبدئي اتكتب بمساعدة أداة ذكاء اصطناعي. اتفقوا مع الدكتور على طريقة ذكر ده في التقرير والـ README، وكل عضو لازم يكون قادر يشرح الجزء بتاعه بنفسه.
