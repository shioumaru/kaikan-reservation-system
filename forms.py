from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email

class ReservationForm(FlaskForm):
    meeting_name = StringField('会合名', validators=[DataRequired()])
    organizer_name = StringField('会合責任者', validators=[DataRequired()])
    phone_number = StringField('電話番号', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    start_time = DateTimeField('使用開始日時', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeField('使用終了日時', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('予約')
