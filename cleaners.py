import os
from PIL import Image
from pypdf import PdfReader, PdfWriter
from docx import Document

def clean_image_metadata(input_path: str, output_path: str) -> bool:
    """Удаляет EXIF-метаданные из изображений (JPEG, PNG)."""
    try:
        with Image.open(input_path) as img:
            # Создаем "чистую" копию изображения без метаданных (data)
            data = list(img.getdata())
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(data)
            clean_img.save(output_path)
        return True
    except Exception as e:
        print(f"Ошибка при очистке изображения {input_path}: {e}")
        return False

def clean_pdf_metadata(input_path: str, output_path: str) -> bool:
    """Удаляет метаданные из PDF-файлов."""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Копируем страницы без метаданных документа
        for page in reader.pages:
            writer.add_page(page)

        # Очищаем метаданные документа (Author, Creator, Producer и т.д.)
        writer.add_metadata({})

        with open(output_path, "wb") as f:
            writer.write(f)
        return True
    except Exception as e:
        print(f"Ошибка при очистке PDF {input_path}: {e}")
        return False

def clean_docx_metadata(input_path: str, output_path: str) -> bool:
    """Удаляет встроенные свойства (метаданные) из документов Word."""
    try:
        doc = Document(input_path)
        
        # Убираем основные встроенные свойства ядра документа
        core_props = doc.core_properties
        core_props.author = ""
        core_props.category = ""
        core_props.comments = ""
        core_props.identifier = ""
        core_props.keywords = ""
        core_props.last_modified_by = ""
        core_props.revision = 1
        core_props.subject = ""
        core_props.title = ""

        doc.save(output_path)
        return True
    except Exception as e:
        print(f"Ошибка при очистке DOCX {input_path}: {e}")
        return False