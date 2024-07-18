from flask import Flask, render_template, jsonify, request
import stripe
import os

app = Flask(__name__)

stripe.api_key = 'api key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': data['currency'],
                    'product_data': {
                        'name': data['name'],
                    },
                    'unit_amount': int(float(data['price']) * 100), 
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
            phone_number_collection={
                'enabled': True,
            },
        )
        return jsonify({'id': session.id})
    except Exception as e:
        print(f"Error creating checkout session: {e}")
        return jsonify(error=str(e)), 500

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return 'Payment canceled'

if __name__ == '__main__':
    app.run(debug=True)
