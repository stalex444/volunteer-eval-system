#!/usr/bin/env python3
"""
Send evaluation reminders to GLs after an event
Usage: python send_reminders.py
"""

from app_new import create_app
from utils.notifications import send_bulk_reminders
from datetime import datetime, timedelta

def send_reminders():
    """Send evaluation reminders to GLs"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Send Evaluation Reminders")
        print("=" * 60)
        print()
        
        # Get event details
        event_name = input("Event name (e.g., 'WLR October 2025'): ")
        
        # Get deadline
        days = input("Days until deadline (default: 3): ").strip()
        days = int(days) if days else 3
        deadline_date = datetime.now() + timedelta(days=days)
        deadline = deadline_date.strftime("%B %d, %Y")
        
        print()
        print("Enter GL emails and names (one per line)")
        print("Format: email,name")
        print("Example: john@example.com,John Smith")
        print("Press Enter twice when done:")
        print()
        
        gl_list = []
        while True:
            line = input().strip()
            if not line:
                break
            
            try:
                email, name = line.split(',')
                gl_list.append({
                    'email': email.strip(),
                    'name': name.strip()
                })
            except ValueError:
                print(f"⚠️  Invalid format: {line}")
                continue
        
        if not gl_list:
            print("❌ No GLs entered!")
            return
        
        print()
        print("=" * 60)
        print(f"Sending reminders to {len(gl_list)} GLs...")
        print("=" * 60)
        print()
        
        # Send reminders
        results = send_bulk_reminders(
            gl_list=gl_list,
            event_name=event_name,
            deadline=deadline
        )
        
        print()
        print("=" * 60)
        print("Results:")
        print("=" * 60)
        print(f"✅ Sent: {results['sent']}")
        print(f"❌ Failed: {results['failed']}")
        
        if results['errors']:
            print()
            print("Failed emails:")
            for email in results['errors']:
                print(f"  - {email}")
        
        print()
        print("📧 Emails sent with:")
        print("  ✓ Evaluation form link")
        print("  ✓ QR code for mobile")
        print(f"  ✓ Deadline: {deadline}")
        print()

if __name__ == '__main__':
    send_reminders()
