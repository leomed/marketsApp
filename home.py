import csv
from flask import Flask, render_template, redirect , url_for
import pandas as pd
from prices import Prices
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, Length
from flask_bootstrap import Bootstrap5


data = pd.read_csv("cafe-data.csv")

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/data")
def data():
        with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = []
            for row in csv_data:
                print(row)
                list_of_rows.append(row)


        # df = pd.read_csv('cafe-data.csv', encoding='utf-8')
        #
        # header = df.columns.tolist()
        # print(header)
        #
        #
        # list_of_rows = []
        # list_of_rows.append(header)
        # for index, row in df.iterrows():
        #     row_as_list = [str(element) for element in row]
        #     list_of_rows.append(row_as_list)

        return render_template('data.html', new_market=list_of_rows)


@app.route("/add", methods=['POST', 'GET'])
def add():
    class Form(FlaskForm):
        market_name = StringField(label='Market Name', validators=[DataRequired()])
        market_location = StringField(label='Market location', validators=[DataRequired(), URL()])
        market_open = StringField(label='Market open', validators=[DataRequired()])
        market_close = StringField(label='Market close', validators=[DataRequired()])
        market_prices = SelectField(label='Market prices', validators=[DataRequired()] , choices=["💪","💪💪","💪💪💪","💪💪💪💪"])
        market_wifi = StringField(label='Market wifi', validators=[DataRequired()])
        market_power = StringField(label='Market power', validators=[DataRequired()])
        submit = SubmitField(label="Add")

    form = Form()

    if form.validate_on_submit():
        with open("cafe-data.csv", "a", newline='', encoding='utf-8') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')

            csv_file.write(f'\n{form["market_name"].data},'
                            f'{form["market_location"].data},'
                            f'{form["market_open"].data},'
                            f'{form["market_close"].data},'
                            f' {form["market_prices"].data},'
                            f' {form["market_power"].data},'
                                )
            return redirect(url_for('data'))
    return render_template("add.html", form=form)


app.secret_key = "123"
if __name__ == '__main__':
    app.run(debug=True)
