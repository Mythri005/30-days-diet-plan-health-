from db_setup import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Integer, nullable=False)  # 0: Male, 1: Female, etc.
    weight = db.Column(db.Float, nullable=True)
    low_bp = db.Column(db.Boolean, nullable=True)
    high_bp = db.Column(db.Boolean, nullable=True)
    sugar = db.Column(db.Integer, nullable=True)  # Blood sugar level
    diabetes = db.Column(db.Boolean, nullable=True)
    heart_disease = db.Column(db.Boolean, nullable=True)
    menstrual_health = db.Column(db.Boolean, nullable=True)
    recommended_diet = db.Column(db.JSON, nullable=True)  # Diet recommendation

    def __repr__(self):
        return f'<User {self.id}, Age: {self.age}, Gender: {self.gender}>'
