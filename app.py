from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def password_complexity_checker(password):
    length_criteria = len(password) >= 8
    uppercase_criteria = any(char.isupper() for char in password)
    lowercase_criteria = any(char.islower() for char in password)
    number_criteria = any(char.isdigit() for char in password)
    special_char_criteria = any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in password)

    criteria_met = {
        "Length (at least 8 characters)": length_criteria,
        "Uppercase letter": uppercase_criteria,
        "Lowercase letter": lowercase_criteria,
        "Number": number_criteria,
        "Special character": special_char_criteria
    }

    score = sum(criteria_met.values())
    if score == 5:
        strength = "Very Strong"
    elif score == 4:
        strength = "Strong"
    elif score == 3:
        strength = "Moderate"
    elif score == 2:
        strength = "Weak"
    else:
        strength = "Very Weak"

    feedback = f"Password Strength: {strength}\n"
    for criterion, met in criteria_met.items():
        feedback += f" - {criterion}: {'Yes' if met else 'No'}\n"

    return feedback

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    feedback = password_complexity_checker(password)
    return jsonify(feedback=feedback)

@app.route('/suggest_password', methods=['GET'])
def suggest_password():
    password = generate_strong_password()
    return jsonify(password=password)

if __name__ == '__main__':
    app.run(debug=True)
