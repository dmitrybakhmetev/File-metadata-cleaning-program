import argparse
import os
from cleaners import clean_image_metadata, clean_pdf_metadata, clean_docx_metadata

def main():
    parser = argparse.ArgumentParser(description="CLI утилита для очистки метаданных файлов.")
    parser.add_argument("file", help="Путь к файлу для очистки метаданных")
    parser.add_argument("-o", "--output", help="Путь для сохранения очищенного файла (необязательно)")

    args = parser.parse_args()
    input_path = args.file

    if not os.path.exists(input_path):
        print(f"Ошибка: файл '{input_path}' не найден.")
        return

    # Определяем выходной путь, если он не задан
    if args.output:
        output_path = args.output
    else:
        dir_name, file_name = os.path.split(input_path)
        output_path = os.path.join(dir_name, f"cleaned_{file_name}")

    # Определяем расширение файла
    ext = os.path.splitext(input_path)[1].lower()

    success = False
    if ext in [".jpg", ".jpeg", ".png"]:
        print(f"Очистка изображения: {input_path}...")
        success = clean_image_metadata(input_path, output_path)
    elif ext == ".pdf":
        print(f"Очистка PDF документа: {input_path}...")
        success = clean_pdf_metadata(input_path, output_path)
    elif ext == ".docx":
        print(f"Очистка Word документа: {input_path}...")
        success = clean_docx_metadata(input_path, output_path)
    else:
        print(f"Неподдерживаемый формат файла: {ext}")
        return

    if success:
        print(f"Успешно! Очищенный файл сохранен как: {output_path}")

if __name__ == "__main__":
    main()