# Users Table Schema Update

## Overview

The users table has been simplified by removing the email field and changing the default role to 'admin'.

## Schema Changes

### Old Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'viewer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### New Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'admin',  -- admin, viewer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Key Changes

1. **Removed Field**: `email` - No longer required
2. **Default Role**: Changed from `'viewer'` to `'admin'`
3. **Simplified**: Only username and password needed

## Model Updates

### Updated User Model

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')  # admin, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

## User Roles

### Admin
- Full access to all features
- Can create/edit/delete data
- Can manage users
- Can view all reports

### Viewer
- Read-only access
- Can view dashboard
- Can view reports
- Cannot modify data

## Flask CLI Commands

### Create Admin User
```bash
flask create-admin
```
Prompts:
- Username
- Password

Creates user with 'admin' role.

### Create Any User
```bash
flask create-user
```
Prompts:
- Username
- Password
- Role (admin/viewer) - defaults to admin

### List All Users
```bash
flask list-users
```

Output:
```
System Users:
----------------------------------------------------------------------
ID    Username             Role       Created
----------------------------------------------------------------------
1     admin                admin      2024-11-02
2     john_viewer          viewer     2024-11-02
3     sarah_admin          admin      2024-11-03
----------------------------------------------------------------------
Total: 3 users
```

## Usage Examples

### Create Admin User

```python
from models import db, User

user = User(username='admin', role='admin')
user.set_password('secure_password')
db.session.add(user)
db.session.commit()
```

### Create Viewer User

```python
from models import db, User

user = User(username='viewer', role='viewer')
user.set_password('secure_password')
db.session.add(user)
db.session.commit()
```

### Query Users

```python
# Get all admins
admins = User.query.filter_by(role='admin').all()

# Get all viewers
viewers = User.query.filter_by(role='viewer').all()

# Find user by username
user = User.query.filter_by(username='admin').first()

# Check password
if user and user.check_password('password'):
    print('Login successful')
```

### Update User Role

```python
user = User.query.filter_by(username='john').first()
user.role = 'admin'
db.session.commit()
```

## Migration Process

### For New Installations

```bash
./setup.sh
flask init-db
flask run-migrations
flask create-admin
flask run
```

### For Existing Installations

```bash
# Backup database
cp database/volunteers.db database/volunteers.db.backup

# Run migration
flask run-migrations

# Verify users
flask list-users
```

The migration will:
1. Create new users table without email field
2. Copy existing users (username, password_hash, role)
3. Drop old table
4. Rename new table

**Note**: Email data will be lost during migration.

## Breaking Changes

### Code That Will Break

1. **Email references**: `user.email` → No longer available
2. **User creation**: Remove email parameter
3. **Forms**: Remove email input fields
4. **API responses**: Don't return email field

### Update Required In

- [ ] User creation forms
- [ ] User profile displays
- [ ] API endpoints
- [ ] Templates showing user info
- [ ] Any email-based functionality

## Authentication

### Login Process

```python
from flask_login import login_user

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('dashboard.index'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))
```

### Login Form

```html
<form method="POST" action="/login">
    <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" required>
    </div>
    
    <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" required>
    </div>
    
    <button type="submit">Login</button>
</form>
```

## Security Considerations

1. **Password Hashing**: Uses Werkzeug's secure password hashing
2. **Unique Usernames**: Enforced at database level
3. **Session Management**: Handled by Flask-Login
4. **Role-Based Access**: Check user.role before allowing actions

### Implementing Role-Based Access

```python
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)
```

## Testing

### Test User Creation

```bash
# Create admin
flask create-admin
# Enter: admin / password123

# Create viewer
flask create-user
# Enter: viewer / password123 / viewer

# List users
flask list-users
```

### Test Login

```python
# In Python shell
from models import db, User

user = User.query.filter_by(username='admin').first()
print(user.check_password('password123'))  # Should return True
print(user.check_password('wrong'))        # Should return False
```

## Best Practices

1. **Strong Passwords**: Enforce minimum length and complexity
2. **Unique Usernames**: Already enforced by database
3. **Role Validation**: Always validate role is 'admin' or 'viewer'
4. **Session Security**: Use secure session cookies in production
5. **Password Reset**: Implement if needed (requires email or alternative)

## Future Enhancements

- [ ] Add password reset functionality
- [ ] Add user profile management
- [ ] Add activity logging
- [ ] Add last login timestamp
- [ ] Add account status (active/inactive)
- [ ] Add password expiration
- [ ] Add two-factor authentication

## Rollback

If you need to rollback:

```bash
# Restore backup
rm database/volunteers.db
cp database/volunteers.db.backup database/volunteers.db

# Revert code changes
git checkout models.py app.py
```

## Support

For questions:
1. Review this documentation
2. Check migration file: `migrations/006_update_users_schema.sql`
3. Test on development environment first
4. Use `flask list-users` to verify users

---

**Status**: ✅ Users table simplified - email removed, default role is admin
