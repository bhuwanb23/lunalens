from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Demo user (in production, use a database)
DEMO_USER = {
    "missionId": "isro123",
    "accessCode": "moon@2024"
}

@app.route('/', methods=['GET'])
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LunaLens Flask Backend</title>
        <style>
            body { font-family: Arial, sans-serif; background: #181c24; color: #f3f3f3; margin: 0; padding: 0; }
            .container { max-width: 700px; margin: 40px auto; background: #23283a; border-radius: 12px; box-shadow: 0 4px 24px #0003; padding: 32px; }
            h1 { color: #60a5fa; }
            h2 { color: #a78bfa; }
            code { background: #181c24; color: #fbbf24; padding: 2px 6px; border-radius: 4px; }
            ul { margin-top: 0; }
            .endpoint { color: #4ade80; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 LunaLens Flask Backend</h1>
            <p>This server powers the LunaLens web application, providing API endpoints for authentication and (future) lunar data analysis.</p>
            <h2>Available API Endpoints</h2>
            <ul>
                <li><span class="endpoint">POST <code>/login</code></span> — User login (expects <code>missionId</code> and <code>accessCode</code> in JSON)</li>
            </ul>
            <h2>How it works</h2>
            <ul>
                <li>Handles <b>API calls</b> from the React frontend</li>
                <li>Authenticates users (demo: hardcoded credentials)</li>
                <li>Ready for <b>database integration</b> (future)</li>
                <li>Can be extended for lunar data, mission logs, and more</li>
            </ul>
            <h2>Demo Credentials</h2>
            <ul>
                <li>Mission ID: <code>isro123</code></li>
                <li>Access Code: <code>moon@2024</code></li>
            </ul>
            <p style="margin-top:32px; color:#94a3b8;">&copy; 2024 LunaLens | ISRO Mission Control</p>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mission_id = data.get('missionId')
    access_code = data.get('AccessCode')

    if mission_id == DEMO_USER['missionId'] and access_code == DEMO_USER['accessCode']:
        return jsonify({"success": True, "message": "Login successful!"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
