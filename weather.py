import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
        
        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

        cities = City.query.all()
        print(cities)
        url = f"https://api.weatherapi.com/v1/current.json?key=99f4cccd0bdb4da3853172939210812&q={new_city}"

        r = requests.get(url).json()
        weather = {
            'city' : new_city,
            'temperature' : r['current']['temp_c'],
            'description' : r['current']['condition']['text'],
            'icon' : r['current']['condition']['icon'],
        }

        return render_template('index.html',weather=weather)
    else:
        return render_template('index.html',weather=False)


    

if __name__ == "__main__":
    app.run(debug=True)