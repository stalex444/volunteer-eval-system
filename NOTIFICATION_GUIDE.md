# How to Notify GLs to Submit Evaluations

## Option 1: Telegram Message (Recommended)

Since you use Telegram for communication, send this message after each event:

```
🎯 **Evaluation Reminder**

Hi GLs! 👋

The [EVENT_NAME] has concluded. Please take 5 minutes to evaluate your volunteers.

📝 Evaluation Form: http://localhost:5001/evaluate

**What to do:**
1. Click the link above
2. Select the volunteer you worked with
3. Rate them on 5 categories (1-10 scale)
4. Add any feedback (optional but helpful!)
5. Submit

⏰ Please complete by [DEADLINE]

Thank you for helping us improve our volunteer program! 🙏
```

## Option 2: Email Template

If you want to send emails, here's a template:

**Subject:** Please Evaluate Your Volunteers - [EVENT_NAME]

**Body:**
```
Hi [GL_NAME],

Thank you for leading at [EVENT_NAME]!

Please take a few minutes to evaluate the volunteers you worked with. Your feedback helps us:
- Recognize top performers
- Identify who needs support
- Improve our volunteer program

📝 Evaluation Form: http://localhost:5001/evaluate

The form takes about 3-5 minutes per volunteer and includes:
- 5 rating categories (Reliability, Quality, Initiative, Teamwork, Communication)
- Optional feedback sections

Please complete your evaluations by [DEADLINE].

Thank you!
[YOUR_NAME]
Volunteer Coordinator
```

## Option 3: Automated Reminders (Future Enhancement)

If you want automated reminders, we can add:
1. Email integration (SendGrid, Mailgun)
2. Scheduled reminders
3. Event tracking
4. Automatic notifications after events

Let me know if you want me to implement this!

## Quick Checklist After Each Event:

- [ ] Event concludes
- [ ] Send Telegram/Email to all GLs
- [ ] Include evaluation link
- [ ] Set deadline (e.g., 3 days)
- [ ] Follow up with non-responders
- [ ] Review submissions in dashboard

## Dashboard Access for GLs:

**View-Only Access:**
- GLs can login to view evaluations
- Cannot edit or delete
- Can see their own submissions
- Can view volunteer performance

**To create GL viewer account:**
```bash
python add_viewer.py
```

Then share credentials via Telegram (securely!)
