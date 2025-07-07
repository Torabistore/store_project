import os
import re

# مسیر اصلی پروژه‌ات؛ می‌تونی متناسب با مسیر واقعی‌ت تغییر بدی
ROOT = "D:/store_project"
TEMPLATE_FOLDER = "templates"
TARGET_EXTENSIONS = (".html",)

def inject_load_tag(content):
    if "{% load price_filters %}" in content:
        return content
    # بعد از اولین خط {% load static %} اضافه می‌کنیم
    pattern = r"(\{\%\s*load\s+static\s*\%\})"
    return re.sub(pattern, r"\1\n{% load price_filters %}", content, count=1)

def replace_price_filters(content):
    # نمایش ساده قیمت → price_format
    content = re.sub(r"(\{\{\s*[^\}]+?price\s*\}\})", lambda m: f"{{{{ {m.group(1)[2:-2].strip()}|price_format }}}}", content)

    # اگر از floatformat استفاده شده:
    content = re.sub(r"\|\s*floatformat\s*:\s*[\"\']?0[\"\']?", "|price_format", content)

    # حذف تومان‌های تکراری که دستی اضافه شدن
    content = re.sub(r"\|price_format\s*\}\}\s*تومان", "}}", content)

    return content

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    content = inject_load_tag(content)
    content = replace_price_filters(content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ فایل اصلاح شد: {filepath}")
    else:
        print(f"⏩ بدون تغییر: {filepath}")

def scan_templates():
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, TEMPLATE_FOLDER)):
        for filename in filenames:
            if filename.endswith(TARGET_EXTENSIONS):
                process_file(os.path.join(dirpath, filename))

if __name__ == "__main__":
    scan_templates()
