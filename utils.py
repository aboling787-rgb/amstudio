import os
from config import ALLOWED_EXTENSIONS
def validate_file(file_name):
    """
    التحقق من أن الملف ضمن التنسيقات المدعومة
    """
    ext = file_name.split('.')[-1].lower()
    return ext in ALLOWED_EXTENSIONS
def human_readable_size(size):
    """
    تحويل عدد البايت إلى صيغة سهلة
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
