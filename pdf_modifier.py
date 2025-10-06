from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from PyPDF2 import PdfReader, PdfWriter
import os

def modify_pdf(filename, cpf, position, color, upload_folder):
    try:
        # Cria um PDF temporário com o CPF desenhado
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        # Define as coordenadas conforme a posição
        if position == 'top-left':
            x, y = 50, 800
        elif position == 'top-right':
            x, y = 500, 800
        elif position == 'bottom-left':
            x, y = 50, 50
        elif position == 'bottom-right':
            x, y = 500, 50
        else:
            raise ValueError('Invalid position')

        # Define a cor e escreve o CPF
        try:
            can.setFillColor(HexColor(color))
        except Exception:
            raise ValueError("Invalid color format. Use hexadecimal, e.g., '#FF5733'.")

        can.setFont("Helvetica", 8)
        can.drawString(x, y, cpf)
        can.save()

        # Cria novo PDF em memória
        packet.seek(0)
        new_pdf = PdfReader(packet)
        print("✅ Successfully created new PDF with CPF.")

    except Exception as e:
        print("❌ Error creating new PDF with CPF:", e)
        return None

    try:
        # Abre o PDF original existente
        input_path = os.path.join(upload_folder, filename)
        existing_pdf = PdfReader(open(input_path, "rb"))
        print("✅ Successfully opened existing PDF.")

        output = PdfWriter()
        print(f"📄 Number of pages in existing PDF: {len(existing_pdf.pages)}")

        # Mescla cada página do original com o texto do novo PDF
        for page in existing_pdf.pages:
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

        # Cria nome novo para não sobrescrever
        output_filename = f"modified_{os.path.basename(filename)}"
        output_path = os.path.join(upload_folder, output_filename)

        with open(output_path, "wb") as outputStream:
            output.write(outputStream)

        print(f"✅ Modified PDF saved at: {output_path}")
        return output_path

    except Exception as e:
        print("❌ Error opening or merging existing PDF:", e)
        return None
