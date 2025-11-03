import requests
from models import db, Volunteer
from config import Config
from datetime import datetime

def import_from_smartsheet():
    """Import volunteer data from Smartsheet"""
    if not Config.SMARTSHEET_API_TOKEN or not Config.SMARTSHEET_SHEET_ID:
        raise ValueError("Smartsheet API credentials not configured")
    
    headers = {
        'Authorization': f'Bearer {Config.SMARTSHEET_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.smartsheet.com/2.0/sheets/{Config.SMARTSHEET_SHEET_ID}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Process rows and create/update volunteers
        imported_count = 0
        updated_count = 0
        
        for row in data.get('rows', []):
            volunteer_data = parse_smartsheet_row(row, data.get('columns', []))
            
            if volunteer_data:
                volunteer = Volunteer.query.filter_by(
                    smartsheet_id=volunteer_data['smartsheet_id']
                ).first()
                
                if volunteer:
                    # Update existing
                    for key, value in volunteer_data.items():
                        setattr(volunteer, key, value)
                    updated_count += 1
                else:
                    # Create new
                    volunteer = Volunteer(**volunteer_data)
                    db.session.add(volunteer)
                    imported_count += 1
        
        db.session.commit()
        
        return {
            'success': True,
            'imported': imported_count,
            'updated': updated_count
        }
        
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'error': str(e)
        }

def parse_smartsheet_row(row, columns):
    """Parse a Smartsheet row into volunteer data"""
    # Map column names to database fields
    column_map = {
        'Name': 'name',
        'Email': 'email',
        'Phone': 'phone',
        'Department': 'department',
        'Role': 'role',
        'Start Date': 'start_date',
        'Status': 'status'
    }
    
    volunteer_data = {'smartsheet_id': str(row['id'])}
    
    for cell in row.get('cells', []):
        column_id = cell.get('columnId')
        column = next((c for c in columns if c['id'] == column_id), None)
        
        if column and column['title'] in column_map:
            field_name = column_map[column['title']]
            value = cell.get('value')
            
            if field_name == 'start_date' and value:
                volunteer_data[field_name] = datetime.strptime(value, '%Y-%m-%d').date()
            else:
                volunteer_data[field_name] = value
    
    return volunteer_data if 'name' in volunteer_data else None
