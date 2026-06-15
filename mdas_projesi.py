from flask import Flask, render_template, request, redirect, url_for
import os
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from io import StringIO

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super_secret_key'

# --- GOOGLE SHEETS API AYARLARI ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

google_sayfasi = None
google_api_error = None

try:
    # Load credentials from environment variable
    creds_b64 = os.getenv('GOOGLE_CREDENTIALS_B64')
    
    if not creds_b64:
        raise ValueError(
            "GOOGLE_CREDENTIALS_B64 environment variable not found. "
            "Please ensure .env file exists and contains GOOGLE_CREDENTIALS_B64."
        )
    
    # Decode base64 credentials
    creds_json_str = base64.b64decode(creds_b64).decode('utf-8')
    creds_dict = json.loads(creds_json_str)
    
    # Create credentials from the dictionary
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # !!! BURAYA GOOGLE DRIVE'DA OLUŞTURDUĞUN E-TABLONUN TAM ADINI YAZ !!!
    google_sayfasi = client.open("MDAS_Hasta_Raporlari").sheet1
    
    # Eğer tablonun içi tamamen boşsa ilk satıra başlıkları otomatik yazıyoruz
    if not google_sayfasi.row_values(1):
        google_sayfasi.append_row([
            "Hasta Adı Soyadı", 
            "Soru 1 Puanı", "Soru 2 Puanı", "Soru 3 Puanı", "Soru 4 Puanı", "Soru 5 Puanı", 
            "Toplam MDAS Skoru"
        ])
except Exception as e:
    google_api_error = str(e)
    print(f"Google API Bağlantı Hatası: {google_api_error}")


@app.route('/')
def index():
    return redirect(url_for('mdas_form'))


# --- HASTANIN QR KODLA GİRDİĞİ ANKET FORMU ---
@app.route('/mdas', methods=['GET', 'POST'])
def mdas_form():
    if request.method == 'POST':
        try:
            patient_name = request.form.get('patient_name', '').strip()
            if not patient_name:
                return "Hata: Hasta adi ve soyadi bos birakilamaz!", 400
            
            q1 = int(request.form.get('q1', 3))
            q2 = int(request.form.get('q2', 3))
            q3 = int(request.form.get('q3', 3))
            q4 = int(request.form.get('q4', 3))
            q5 = int(request.form.get('q5', 3))
            
            total_score = q1 + q2 + q3 + q4 + q5
            
            if google_sayfasi is None:
                error_message = (
                    "Google Sheets bağlantısı kurulamadı. \n"
                    "sunucu günlüklerini kontrol edin ve anahtar dosyasının doğru olduğundan emin olun."
                )
                if google_api_error:
                    error_message += f"\nDetay: {google_api_error}"
                return error_message, 500

            # --- BULUT OTOMASYONU: DOĞRUDAN GOOGLE SHEETS'E EKLEME ---
            yeni_satir = [patient_name, q1, q2, q3, q4, q5, total_score]
            google_sayfasi.append_row(yeni_satir)
            
            return render_template('result.html', score=total_score, already_done=False)
            
        except Exception as e:
            return f"Veri buluta yazılırken bir hata oluştu: {str(e)}", 400

    return render_template('form.html')


# --- CANLI BULUT RAPOR PANELİ ---
@app.route('/rapor')
def rapor_sayfasi():
    if google_sayfasi is None:
        error_message = (
            "Google Sheets bağlantısı kurulamadı, rapor sayfası yüklenemiyor.\n"
            "Sunucu günlüklerinde bağlantı hatasını kontrol edin."
        )
        if google_api_error:
            error_message += f"\nDetay: {google_api_error}"
        return error_message, 500

    # Tüm verileri Google Sheets'ten anlık canlı olarak çekiyoruz
    veriler = google_sayfasi.get_all_records()
    
    html_icerik = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MDAS Canlı Bulut Raporu</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light p-5">
        <div class="container bg-white p-4 rounded shadow-sm">
            <h2 class="text-primary mb-4">☁️ MDAS Google Sheets Canlı Rapor Paneli</h2>
            <p class="text-muted small">Bu sayfadaki veriler doğrudan Google Drive üzerindeki e-tablodan anlık çekilmektedir.</p>
            
            <table class="table table-striped table-hover border align-middle">
                <thead class="table-primary">
                    <tr>
                        <th>Hasta Adı Soyadı</th>
                        <th>S1</th><th>S2</th><th>S3</th><th>S4</th><th>S5</th>
                        <th>Toplam Skor</th>
                    </tr>
                </thead>
                <tbody>
    """
    for h in veriler:
        html_icerik += f"""
                    <tr>
                        <td class="fw-bold">{h.get('Hasta Adı Soyadı')}</td>
                        <td>{h.get('Soru 1 Puanı')}</td>
                        <td>{h.get('Soru 2 Puanı')}</td>
                        <td>{h.get('Soru 3 Puanı')}</td>
                        <td>{h.get('Soru 4 Puanı')}</td>
                        <td>{h.get('Soru 5 Puanı')}</td>
                        <td class="text-danger fw-bold">{h.get('Toplam MDAS Skoru')}</td>
                    </tr>
        """
    html_icerik += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_icerik

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)