from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging

app = Flask(__name__)

# Enable CORS for specific origins
CORS(app, resources={r"/api/*": {"origins": ["http://trusteddomain1.com", "http://trusteddomain2.com"]}})

# Set up logging
logging.basicConfig(level=logging.INFO)

# Allowed bank accounts
ALLOWED_ACCOUNTS = ['1976278463', '20057942287']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send_sec', methods=['POST'])
def send_sec():
    try:
        data = request.get_json()
        
        if not data:
            app.logger.error('No data received')
            return jsonify({'error': 'No data received'}), 400
        
        bank_account = data.get('bank_account')
        converted_sec = data.get('converted_sec')

        if not bank_account or not converted_sec:
            app.logger.error('Missing required fields')
            return jsonify({'error': 'Missing required fields'}), 400

        if bank_account not in ALLOWED_ACCOUNTS:
            app.logger.error(f'Account {bank_account} is not allowed')
            return jsonify({'error': f'Account {bank_account} is not allowed'}), 403

        # Process the converted_sec value (activate it)
        activated_sec = activate_sec(converted_sec)

        # Simulate sending to account
        success = simulate_send_to_account(bank_account, activated_sec)

        if success:
            # Log successful transaction
            app.logger.info(f'Transaction successful for account {bank_account}')
            return jsonify({'success': True, 'message': 'Transaction successful'}), 200
        else:
            app.logger.error('Failed to send to account')
            return jsonify({'success': False, 'error': 'Failed to send to account'}), 500
    except Exception as e:
        app.logger.error(f'An error occurred: {e}')
        return jsonify({'success': False, 'error': 'An internal error occurred'}), 500

def activate_sec(converted_sec):
    # Activate the sec (this is just a placeholder for actual activation logic)
    # Assuming the activation logic involves some transformation or processing
    return converted_sec * 1.1  # Example: increase by 10%

def simulate_send_to_account(bank_account, activated_sec):
    # Simulate sending to account logic
    # For this example, we'll assume success if bank_account is allowed and activated_sec is a positive number
    if bank_account in ALLOWED_ACCOUNTS and isinstance(activated_sec, (int, float)) and activated_sec > 0:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
