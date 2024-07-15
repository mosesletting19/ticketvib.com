import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import qrcode
import io

def send_email_with_qr_code(name, email, event):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'{name}, {email}, {event["title"]}')
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'
    msg['To'] = email
    msg['Subject'] = 'Your Event Access Code'

    text = f'Hello {name},\n\nYou are invited to the event: {event["title"]}.\n\nDetails:\nDate: {event["date"]}\nVenue: {event["venue"]}\nDescription: {event["description"]}\n\nPlease find the QR code attached for entry.\n\nBest regards,\nEvent Team'
    msg.attach(MIMEText(text))

    image = MIMEImage(img_byte_arr.getvalue(), name='qrcode.png')
    msg.attach(image)

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login('your_email@example.com', 'your_password')
            server.send_message(msg)
    except Exception as e:
        print(f'Error sending email: {e}')
