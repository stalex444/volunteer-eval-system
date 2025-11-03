# Email Setup Guide

## 📧 Automated Email Reminders with QR Codes

Your system now includes:
- ✅ Automated email reminders
- ✅ QR codes for mobile scanning
- ✅ Beautiful HTML emails
- ✅ Bulk sending to multiple GLs

## Setup Instructions

### 1. Install Dependencies

```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
pip install -r requirements.txt
```

### 2. Configure Email Settings

Create a `.env` file in your project root:

```bash
# Gmail Example (Recommended for testing)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Or use SendGrid (Production)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

### 3. Gmail App Password Setup

If using Gmail:
1. Go to Google Account settings
2. Security → 2-Step Verification (enable it)
3. App passwords → Generate new password
4. Copy the 16-character password
5. Use it in `.env` file

### 4. Send Reminders After an Event

```bash
python send_reminders.py
```

**Example interaction:**
```
Event name: WLR October 2025
Days until deadline: 3

Enter GL emails and names:
john@example.com,John Smith
sarah@example.com,Sarah Johnson
mike@example.com,Mike Chen

[Press Enter]

✅ Sent: 3
```

## 📱 QR Code Feature

**Why QR codes are GREAT here:**
- ✅ GLs can scan with phone camera
- ✅ Instant access to form
- ✅ No typing URLs
- ✅ Works offline (opens when connected)
- ✅ Professional look

**Email includes:**
1. Clickable button link
2. QR code image (scannable)
3. Plain text URL (copy/paste)

## Email Template Preview

```
┌─────────────────────────────────────┐
│   🎯 Evaluation Reminder            │
│   Time to evaluate your volunteers! │
└─────────────────────────────────────┘

Hi John,

Thank you for leading at WLR October 2025! 🙏

Please take a few minutes to evaluate...

[Submit Evaluation Now] ← Button

┌─────────────────────────────────────┐
│  📱 Scan to Evaluate on Mobile      │
│                                     │
│      [QR CODE IMAGE]                │
│                                     │
│  Or copy: http://localhost:5001... │
└─────────────────────────────────────┘
```

## Alternative: Telegram Bot (Future)

If you prefer Telegram over email:
- Can send QR codes via Telegram
- Inline buttons
- Automatic reminders
- No email setup needed

Let me know if you want Telegram integration instead!

## Testing

Test email sending:
```bash
python send_reminders.py
```

Enter your own email to test:
```
Event name: Test Event
Days until deadline: 1
your-email@gmail.com,Your Name
```

Check your inbox for the beautiful email with QR code! 📧✨
