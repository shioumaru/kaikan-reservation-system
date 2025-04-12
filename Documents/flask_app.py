from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import logging

# 🔧 ログ出力の設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# 🔑 環境変数の読み込み
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SPREADSHEET_KEY = os.getenv("SPREADSHEET_KEY")
SHEET_NAME = os.getenv("SHEET_NAME")

# Flaskアプリ作成
app = Flask(__name__)

# 📄 Google Sheets API 認証設定
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# 🔄 スプレッドシート接続
spreadsheet = None
worksheet = None
try:
    spreadsheet = client.open_by_key(SPREADSHEET_KEY)
    worksheet = spreadsheet.worksheet(SHEET_NAME)  # 👈 環境変数からシート名を読み込む
    logger.info("Googleスプレッドシートに接続しました。")
except Exception as e:
    logger.error("スプレッドシート接続失敗: %s", e, exc_info=True)

# フォームページ表示
@app.route('/')
def index():
    logger.debug("フォームページにアクセスされました。")
    return render_template('form.html')

# フォーム送信処理
@app.route('/submit', methods=['POST'])
def submit():
    if worksheet is None:
        logger.error("スプレッドシートに接続できませんでした。")
        return "エラー：スプレッドシートに接続できません。", 500

    try:
        # フォームデータを辞書で取得
        data = {
            '管理番号': request.form.get('管理番号', ''),
            'クライアント名': request.form.get('クライアント名', ''),
            '電話番号': request.form.get('電話番号', ''),
            '指示書ナンバー': request.form.get('指示書ナンバー', ''),
            '保護フィルム確認': request.form.get('保護フィルム確認', ''),
            'カードダブ設定確認': request.form.get('カードダブ設定確認', ''),
            'MDM登録': request.form.get('MDM登録', ''),
            '初期化': request.form.get('初期化', ''),
            'SIM挿入確認': request.form.get('SIM挿入確認', ''),
            '作業担当者名': request.form.get('作業担当者名', ''),
            'Wチェック担当者名': request.form.get('Wチェック担当者名', ''),
            '最終チェック責任者名': request.form.get('最終チェック責任者名', ''),
            '進捗状況': request.form.get('進捗状況', ''),
            '完了日時': request.form.get('完了日時', ''),
            '備考': request.form.get('備考', '')
        }

        # スプレッドシートに書き込み
        row_values = [
            data['管理番号'],
            data['クライアント名'],
            data['電話番号'],
            data['指示書ナンバー'],
            data['保護フィルム確認'],
            data['カードダブ設定確認'],
            data['MDM登録'],
            data['初期化'],
            data['SIM挿入確認'],
            data['作業担当者名'],
            data['Wチェック担当者名'],
            data['最終チェック責任者名'],
            data['進捗状況'],
            data['完了日時'],
            data['備考']
        ]
        worksheet.append_row(row_values)
        logger.info("スプレッドシートに書き込み完了。")

        # メール作成と送信
        message = "\n".join([f"{k}: {v}" for k, v in data.items()])
        msg = MIMEText(message)
        msg['Subject'] = '新しいキッティング作業報告'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Date'] = formatdate(localtime=True)

        logger.debug(f"認証に使用するメールアドレス: {EMAIL_ADDRESS}")
        logger.debug(f"認証に使用するパスワード: {EMAIL_PASSWORD}")

        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            logger.error("EMAIL_ADDRESS または EMAIL_PASSWORD が設定されていません。")
            return "エラー：メールアドレスまたはパスワードが設定されていません。", 500

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            logger.info("メール送信に成功しました。")

        return '送信が完了しました！'

    except Exception as e:
        logger.error("送信処理でエラーが発生しました: %s", e, exc_info=True)
        return f"エラーが発生しました: {e}", 500

# アプリ起動
if __name__ == '__main__':
    app.run(debug=True)