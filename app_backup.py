from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from forms import ReservationForm
from models import db, Reservation
from email_handler import send_reservation_email
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(Config)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '12esperanza12@gmail.com'
app.config['MAIL_PASSWORD'] = 'nisd vmzu yewi cuma'  # 生成されたアプリパスワードを入力

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

@app.route('/')
def index():
    reservations = Reservation.query.all()
    return render_template('index.html', reservations=reservations)

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    form = ReservationForm()
    
    # フォームの入力内容をログ出力
    print(f'フォームの入力内容: {form.data}')

    if form.validate_on_submit():
        try:
            reservation = Reservation(
                meeting_name=form.meeting_name.data,
                organizer_name=form.organizer_name.data,
                phone_number=form.phone_number.data,
                email=form.email.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
            )
            db.session.add(reservation)
            db.session.commit()
            print('データベースへの書き込みに成功しました')
        except Exception as e:
            print(f'データベースへの書き込みに失敗しました: {e}')
            flash(f'データベースへの書き込みに失敗しました: {e}')
            return render_template('reserve.html', form=form)

        # メール送信の処理
        try:
            msg = Message('予約確認', sender='12esperanza12@gmail.com', recipients=[form.email.data])
            msg.body = f'以下の内容で予約が完了しました:\n\n会合名: {form.meeting_name.data}\n責任者: {form.organizer_name.data}\n電話番号: {form.phone_number.data}\nメールアドレス: {form.email.data}\n開始日時: {form.start_time.data}\n終了日時: {form.end_time.data}'
            mail.send(msg)
            print('予約確認メールの送信に成功しました')
            
            # 自分自身へのメール送信
            msg_admin = Message('予約確認通知', sender='12esperanza12@gmail.com', recipients=['12esperanza12@gmail.com'])
            msg_admin.body = f'以下の内容で予約が完了しました:\n\n会合名: {form.meeting_name.data}\n責任者: {form.organizer_name.data}\n電話番号: {form.phone_number.data}\nメールアドレス: {form.email.data}\n開始日時: {form.start_time.data}\n終了日時: {form.end_time.data}'
            mail.send(msg_admin)
            print('自分自身への予約確認通知メールの送信に成功しました')

            flash('予約が完了しました！確認のメールが送信されました。')
        except Exception as e:
            print(f'メール送信に失敗しました: {e}')
            flash(f'メール送信に失敗しました: {e}')

        return redirect(url_for('index'))
    else:
        # フォームが正しく検証されなかった場合のログ出力
        for field, errors in form.errors.items():
            for error in errors:
                print(f'Error in the {getattr(form, field).label.text} field - {error}')
        flash('予約フォームの検証に失敗しました。すべての必須フィールドが正しく入力されているか確認してください。')
    return render_template('reserve.html', form=form)

# テストメール送信のエンドポイント
@app.route('/send-test-email')
def send_test_email():
    msg = Message('Test Email', sender='12esperanza12@gmail.com', recipients=['12esperanza12@gmail.com'])  # 有効なメールアドレスを入力
    msg.body = 'This is a test email sent from Flask application.'
    mail.send(msg)
    return 'Test email sent!'

if __name__ == '__main__':
    app.run(debug=True)


