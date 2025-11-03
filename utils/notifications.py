"""
Email notifications and QR code generation
"""
import qrcode
import io
import base64
from flask_mail import Mail, Message
from flask import current_app, url_for

mail = Mail()

def generate_qr_code(url):
    """Generate QR code for evaluation form URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for email embedding
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return img_base64

def send_evaluation_reminder(gl_email, gl_name, event_name, deadline=None):
    """
    Send evaluation reminder email to GL with QR code
    
    Args:
        gl_email: GL's email address
        gl_name: GL's name
        event_name: Name of the event
        deadline: Optional deadline date string
    """
    # Generate evaluation form URL
    eval_url = url_for('evaluation.submit_evaluation', _external=True)
    
    # Generate QR code
    qr_code_base64 = generate_qr_code(eval_url)
    
    # Email subject
    subject = f"Please Evaluate Your Volunteers - {event_name}"
    
    # Email body (HTML)
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
                color: #1e293b;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 12px;
                text-align: center;
                margin-bottom: 30px;
            }}
            .content {{
                background: #f8fafc;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 20px;
            }}
            .button {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin: 20px 0;
            }}
            .qr-section {{
                text-align: center;
                background: white;
                padding: 30px;
                border-radius: 12px;
                margin: 20px 0;
                border: 2px dashed #cbd5e1;
            }}
            .qr-code {{
                max-width: 200px;
                margin: 20px auto;
            }}
            .footer {{
                text-align: center;
                color: #64748b;
                font-size: 14px;
                margin-top: 30px;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Evaluation Reminder</h1>
            <p>Time to evaluate your volunteers!</p>
        </div>
        
        <div class="content">
            <p>Hi {gl_name},</p>
            
            <p>Thank you for leading at <strong>{event_name}</strong>! 🙏</p>
            
            <p>Please take a few minutes to evaluate the volunteers you worked with. Your feedback helps us:</p>
            <ul>
                <li>✨ Recognize top performers</li>
                <li>📈 Identify who needs support</li>
                <li>🎯 Improve our volunteer program</li>
            </ul>
            
            {"<p><strong>⏰ Deadline:</strong> " + deadline + "</p>" if deadline else ""}
            
            <div style="text-align: center;">
                <a href="{eval_url}" class="button">Submit Evaluation Now</a>
            </div>
            
            <p style="margin-top: 30px;"><strong>What to expect:</strong></p>
            <ul>
                <li>Takes 3-5 minutes per volunteer</li>
                <li>Rate 5 categories (1-10 scale)</li>
                <li>Optional feedback sections</li>
                <li>Submit and you're done!</li>
            </ul>
        </div>
        
        <div class="qr-section">
            <h3>📱 Scan to Evaluate on Mobile</h3>
            <p style="color: #64748b;">Use your phone's camera to scan this QR code</p>
            <img src="data:image/png;base64,{qr_code_base64}" class="qr-code" alt="QR Code">
            <p style="font-size: 14px; color: #64748b; margin-top: 15px;">
                Or copy this link: <br>
                <code style="background: #e2e8f0; padding: 5px 10px; border-radius: 4px; font-size: 12px;">
                    {eval_url}
                </code>
            </p>
        </div>
        
        <div class="footer">
            <p>Thank you for your dedication to our volunteer program! 💜</p>
            <p style="font-size: 12px; margin-top: 20px;">
                Questions? Reply to this email or contact your volunteer coordinator.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version (fallback)
    text_body = f"""
    Hi {gl_name},
    
    Thank you for leading at {event_name}!
    
    Please take a few minutes to evaluate the volunteers you worked with.
    
    Evaluation Form: {eval_url}
    
    {"Deadline: " + deadline if deadline else ""}
    
    The form takes about 3-5 minutes per volunteer and includes:
    - 5 rating categories (Reliability, Quality, Initiative, Teamwork, Communication)
    - Optional feedback sections
    
    Thank you for helping us improve our volunteer program!
    """
    
    # Create and send email
    msg = Message(
        subject=subject,
        recipients=[gl_email],
        html=html_body,
        body=text_body
    )
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_bulk_reminders(gl_list, event_name, deadline=None):
    """
    Send evaluation reminders to multiple GLs
    
    Args:
        gl_list: List of dicts with 'email' and 'name' keys
        event_name: Name of the event
        deadline: Optional deadline date string
    
    Returns:
        Dict with success/failure counts
    """
    results = {'sent': 0, 'failed': 0, 'errors': []}
    
    for gl in gl_list:
        success = send_evaluation_reminder(
            gl_email=gl['email'],
            gl_name=gl['name'],
            event_name=event_name,
            deadline=deadline
        )
        
        if success:
            results['sent'] += 1
        else:
            results['failed'] += 1
            results['errors'].append(gl['email'])
    
    return results
