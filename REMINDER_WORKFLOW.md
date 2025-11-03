# 📋 Evaluation Reminder Workflow Guide

You have **two options** for sending evaluation reminders to GLs:

---

## Option A: Quick Telegram Share (Simplest) 📱

**Perfect for:** Quick reminders, small groups, informal communication

### Workflow:

**1. Generate QR Code**
```bash
python generate_qr.py
```
- Creates QR code image in `qr_codes/` folder
- Opens automatically or find at: `qr_codes/evaluation_qr_latest.png`

**2. Share in Telegram**

Post this message in your GL group chat:

```
🎯 Evaluation Time!

Hey team! Please take 5 minutes to evaluate your volunteers from [EVENT NAME].

📝 Evaluation Form: http://localhost:5001/evaluate

[Attach QR code image here]

⏰ Please complete by [DATE]

Scan the QR code with your phone camera or click the link above.

Thanks! 🙏
```

**3. Attach the QR Code**
- Click attachment button in Telegram
- Select `qr_codes/evaluation_qr_latest.png`
- Send!

**4. Track Completions**
- Check dashboard: http://localhost:5001/login
- View "Recent Evaluations"
- Follow up with anyone who hasn't submitted

### Time Required: **30 seconds** ⚡

---

## Option B: Automated Email with QR Code (Professional) 📧

**Perfect for:** Formal communication, bulk sending, audit trail

### One-Time Setup (5 minutes):

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Configure Email**

Create `.env` file in project root:

```bash
# Gmail (Recommended for testing)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**3. Get Gmail App Password**
- Go to: https://myaccount.google.com/security
- Enable 2-Step Verification
- App passwords → Generate
- Copy 16-character password
- Paste in `.env` file

See `EMAIL_SETUP.md` for detailed instructions.

### After Each Event:

**1. Run Script**
```bash
python send_reminders.py
```

**2. Enter Details**
```
Event name: WLR October 2025
Days until deadline: 3

Enter GL emails and names:
john@example.com,John Smith
sarah@example.com,Sarah Johnson
mike@example.com,Mike Chen

[Press Enter twice]
```

**3. Emails Sent!**
```
✅ Sent: 3
📧 Emails sent with:
  ✓ Evaluation form link
  ✓ QR code for mobile
  ✓ Deadline: November 5, 2025
```

**4. GLs Receive Beautiful Email**
- Professional HTML design
- Clickable button
- QR code image
- Deadline reminder
- Instructions

### Time Required: **2 minutes** ⚡

---

## 📊 Comparison

| Feature | Telegram (A) | Email (B) |
|---------|-------------|-----------|
| **Setup Time** | None | 5 min (one-time) |
| **Send Time** | 30 sec | 2 min |
| **Delivery** | Instant | Instant |
| **Spam Risk** | None | Low |
| **QR Code** | ✅ Yes | ✅ Yes |
| **Professional** | Casual | Formal |
| **Audit Trail** | Chat history | Email records |
| **Bulk Send** | Manual | Automated |
| **Best For** | Quick, informal | Professional, bulk |

---

## 🎯 Recommended Workflow

**For Most Events:**
1. Use **Telegram** (Option A) - quick and easy
2. Post in group chat with QR code
3. Check dashboard after deadline
4. Follow up in Telegram if needed

**For Formal Reviews:**
1. Use **Email** (Option B) - professional
2. Send to all GLs at once
3. Automatic QR codes included
4. Email record for documentation

**Hybrid Approach:**
1. Post in Telegram first (quick reminder)
2. Send email 24 hours later (formal follow-up)
3. Best of both worlds!

---

## 📱 QR Code Benefits

**Why QR codes are great:**
- ✅ GLs scan with phone camera
- ✅ No typing URLs
- ✅ Works offline (opens when connected)
- ✅ Professional and modern
- ✅ Accessible for everyone
- ✅ Faster than clicking links

**How GLs use it:**
1. Open phone camera
2. Point at QR code
3. Tap notification
4. Form opens in browser
5. Fill and submit!

---

## 🔄 Complete Event Workflow

### Before Event:
- [ ] Volunteers are in database
- [ ] Dashboard login works
- [ ] Evaluation form tested

### During Event:
- [ ] GLs work with volunteers
- [ ] Note who worked with whom

### After Event (Within 24 hours):

**Option 1: Telegram**
- [ ] Run: `python generate_qr.py`
- [ ] Post message + QR in Telegram
- [ ] Set deadline (e.g., 3 days)

**Option 2: Email**
- [ ] Run: `python send_reminders.py`
- [ ] Enter event details
- [ ] Paste GL emails/names
- [ ] Emails sent automatically

### Follow-Up (Day before deadline):
- [ ] Check dashboard for submissions
- [ ] Message GLs who haven't submitted
- [ ] Extend deadline if needed

### After Deadline:
- [ ] Review all evaluations
- [ ] Check volunteer profiles
- [ ] Identify top performers
- [ ] Note who needs support

---

## 🆘 Quick Reference

**Generate QR Code:**
```bash
python generate_qr.py
```

**Send Email Reminders:**
```bash
python send_reminders.py
```

**Access Dashboard:**
```
http://localhost:5001/login
Username: admin
Password: admin123
```

**Evaluation Form URL:**
```
http://localhost:5001/evaluate
```

**QR Code Location:**
```
qr_codes/evaluation_qr_latest.png
```

---

## 💡 Pro Tips

1. **Save QR code to phone** - Quick access for future events
2. **Pin Telegram message** - Keep evaluation link at top of chat
3. **Set calendar reminder** - Send reminders 1 day after events
4. **Check dashboard daily** - Monitor submission progress
5. **Thank GLs publicly** - Acknowledge completed evaluations

---

## 🎉 You're All Set!

Both systems are ready to use:
- ✅ QR code generator (Telegram sharing)
- ✅ Automated emails (professional option)
- ✅ Beautiful evaluation form
- ✅ Dashboard for tracking

Choose the method that fits your workflow best! 🚀
