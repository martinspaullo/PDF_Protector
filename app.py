from flask import Flask, render_template, request, send_file, flash, redirect
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os
from pdf_modifier import modify_pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['UPLOAD_FOLDER'] = './uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class CPFInputForm(FlaskForm):
    cpf = StringField('CPF', validators=[DataRequired()])
    position = SelectField('Position', choices=[
        ('top-left', 'Top Left'),
        ('top-right', 'Top Right'),
        ('bottom-left', 'Bottom Left'),
        ('bottom-right', 'Bottom Right')
    ])
    color = StringField('Color', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=["GET", "POST"])
def upload_file():
    form = CPFInputForm()

    if request.method == "POST":
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado.')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("Nenhum arquivo selecionado.")
            return redirect(request.url)

        if file and form.validate_on_submit():
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            cpf = form.cpf.data
            position = form.position.data
            color = form.color.data

            try:
                modified_path = modify_pdf(filename, cpf, position, color, app.config["UPLOAD_FOLDER"])
                if modified_path:
                    return send_file(modified_path, as_attachment=True)
                else:
                    flash("Erro ao modificar o PDF.")
            except Exception as e:
                flash(f"Erro ao processar o arquivo: {e}")
                return redirect(request.url)

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
