import os
import uuid
from flask import Flask, render_template, request, send_file, redirect
from cleaners import clean_image_metadata, clean_pdf_metadata, clean_docx_metadata

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Получаем расширение безопасным способом
            ext = file.filename.rsplit('.', 1)[1].lower()
            
            # Генерируем уникальное имя на английском, чтобы избежать проблем с кириллицей
            unique_filename = f"{uuid.uuid4()}.{ext}"
            
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            output_filename = f"cleaned_{unique_filename}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            file.save(input_path)
            
            # Вызываем нужный очиститель в зависимости от формата
            success = False
            if ext in {'jpg', 'jpeg', 'png'}:
                success = clean_image_metadata(input_path, output_path)
            elif ext == 'pdf':
                success = clean_pdf_metadata(input_path, output_path)
            elif ext == 'docx':
                success = clean_docx_metadata(input_path, output_path)
                
            if success and os.path.exists(output_path):
                # Отдаем файл пользователю под понятным именем
                return send_file(output_path, as_attachment=True, download_name=f"cleaned_{file.filename}")
            else:
                return "Ошибка при очистке метаданных файла.", 500
                
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)