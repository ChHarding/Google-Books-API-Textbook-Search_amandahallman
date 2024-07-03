@app.route('/upload_syllabus', methods=['POST'])
def upload_syllabus():
    if 'syllabus' not in request.files:
        return redirect(request.url)
    
    file = request.files['syllabus']
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Process the syllabus with ChatGPT
        processed_syllabus = process_syllabus(filepath)
        return render_template('syllabus_results.html', syllabus=processed_syllabus)
    else:
        return "File type not allowed"
    
def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in {'pdf', 'doc', 'docx', 'txt'}