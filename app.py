from flask import Flask, render_template_string
import subprocess
import datetime
import os
import socket
import pytz

app = Flask(__name__)

@app.route('/htop')
def htop():
    # Get username
    username = os.getenv('USER', subprocess.getoutput('whoami'))
    
    # Get full name (using a fallback if not available)
    try:
        # Try to get the full name from passwd file
        full_name = subprocess.getoutput("getent passwd $USER | cut -d ':' -f 5 | cut -d ',' -f 1")
        if not full_name or full_name.startswith("getent:"):
            full_name = "Your Full Name"  # Fallback
    except:
        full_name = "Your Full Name"  # Fallback
    
    # Get server time in IST
    ist_timezone = pytz.timezone('Asia/Kolkata')
    server_time_ist = datetime.datetime.now(ist_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')
    
    # Get top output
    try:
        top_output = subprocess.check_output(['top', '-b', '-n', '1'], text=True)
    except:
        top_output = "Error fetching top output"
    
    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTOP Endpoint</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .info-section {
                margin-bottom: 20px;
            }
            .info-item {
                margin-bottom: 10px;
            }
            .info-label {
                font-weight: bold;
            }
            pre {
                background-color: #f5f5f5;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <h1>HTOP Endpoint</h1>
        
        <div class="info-section">
            <div class="info-item">
                <span class="info-label">Name:</span> {{ full_name }}
            </div>
            <div class="info-item">
                <span class="info-label">Username:</span> {{ username }}
            </div>
            <div class="info-item">
                <span class="info-label">Server Time in IST:</span> {{ server_time_ist }}
            </div>
        </div>
        
        <h2>Top Output:</h2>
        <pre>{{ top_output }}</pre>
    </body>
    </html>
    """
    
    return render_template_string(html_template, 
                                 full_name=full_name,
                                 username=username,
                                 server_time_ist=server_time_ist,
                                 top_output=top_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
