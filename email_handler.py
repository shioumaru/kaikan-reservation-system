from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_reservation_email(reservation):
    msg = Message('予約確認', recipients=[reservation.email, current_app.config['MAIL_USERNAME']])
    msg.body = f'''
    予約が完了しました。

    会合名: {reservation.meeting_name}
    会合責任者: {reservation.organizer_name}
    電話番号: {reservation.phone_number}
    メールアドレス: {reservation.email}
    使用開始日時: {reservation.start_time.strftime('%Y-%m-%d %H:%M')}
    使用終了日時: {reservation.end_time.strftime('%Y-%m-%d %H:%M')}
    '''
    mail.send(msg)
