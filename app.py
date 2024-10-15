from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodplanner.db'
db = SQLAlchemy(app)

class BreakfastM(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable = False)
    count = db.Column(db.Integer,default=1)
    calories = db.Column(db.Integer,default = 0)

    def __repr__(self):
        return '<%r>' % self.id

class LunchM(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable = False)
    count = db.Column(db.Integer,default=1)
    calories = db.Column(db.Integer,default = 0)

    def __repr__(self):
        return '<%r>' % self.id


class DinnerM(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable = False)
    count = db.Column(db.Integer,default=1)
    calories = db.Column(db.Integer,default = 0)

    def __repr__(self):
        return '<%r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        items_to_add = []

        try:
            # Access form data using correct field names (ensure they match your HTML form)
            brItemContent = request.form['brContent']
            new_brItem = BreakfastM(content=brItemContent)
            items_to_add.append(new_brItem)  # Add successfully created Breakfast item
        except KeyError:
            pass  # Ignore missing 'brContent' field

        try:
            luItemContent = request.form['luContent']
            new_luItem = LunchM(content=luItemContent)  # Use LunchM for lunch items
            items_to_add.append(new_luItem)  # Add successfully created Lunch item
        except KeyError:
            pass  # Ignore missing 'luContent' field

        try:
            diItemContent = request.form['diContent']
            new_diItem = DinnerM(content=diItemContent)  # Use DinnerM for dinner items
            items_to_add.append(new_diItem)  # Add successfully created Dinner item
        except KeyError:
            pass  # Ignore missing 'diContent' field

        try:
            # Add all successfully created items in a single transaction
            db.session.add_all(items_to_add)
            db.session.commit()

            return redirect('/')  # Redirect to the root route after successful addition

        except Exception as e:
            # Handle any database-related exceptions
            print(f"An error occurred: {e}")  # Log the error for debugging
            return 'There was an issue adding your item(s)'  # Provide user-friendly message

    else:  # GET request
        # Fetch all items from their respective models for rendering
        brItems = BreakfastM.query.order_by(BreakfastM.id).all()
        luItems = LunchM.query.order_by(LunchM.id).all()
        diItems = DinnerM.query.order_by(DinnerM.id).all()

        # Pass all items to the template for display
        return render_template("index.html", brItems=brItems, luItems=luItems, diItems=diItems)



@app.route('/brChoose')
def brChoose():

    return render_template('brChoose.html')

@app.route('/luChoose')
def luChoose():

    return render_template('luChoose.html')

@app.route('/diChoose')
def diChoose():

    return render_template('diChoose.html')


if __name__ == '__main__':
    app.run(debug=True)

