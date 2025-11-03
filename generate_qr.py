#!/usr/bin/env python3
"""
Generate QR code for evaluation form
Usage: python generate_qr.py
"""

import qrcode
from datetime import datetime
import os

def generate_qr():
    """Generate QR code image for evaluation form"""
    
    print("=" * 60)
    print("QR Code Generator for Evaluation Form")
    print("=" * 60)
    print()
    
    # Get evaluation form URL
    print("Enter your evaluation form URL:")
    print("(Default: http://localhost:5001/evaluate)")
    url = input("URL: ").strip()
    
    if not url:
        url = "http://localhost:5001/evaluate"
    
    print()
    print(f"Generating QR code for: {url}")
    print()
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create image with custom colors (Dr. Joe gradient colors)
    img = qr.make_image(fill_color="#667eea", back_color="white")
    
    # Create output directory if it doesn't exist
    output_dir = "qr_codes"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/evaluation_qr_{timestamp}.png"
    
    # Save image
    img.save(filename)
    
    # Also save a "latest" version for easy access
    latest_filename = f"{output_dir}/evaluation_qr_latest.png"
    img.save(latest_filename)
    
    print("=" * 60)
    print("✅ QR Code Generated Successfully!")
    print("=" * 60)
    print()
    print(f"📁 Saved to: {filename}")
    print(f"📁 Latest: {latest_filename}")
    print()
    print("📱 How to use:")
    print("  1. Open the image file")
    print("  2. Share in Telegram group chat")
    print("  3. GLs scan with phone camera")
    print("  4. Opens evaluation form automatically!")
    print()
    print("💡 Tip: The 'latest' file always has the same name,")
    print("   so you can bookmark it for quick access!")
    print()

if __name__ == '__main__':
    generate_qr()
