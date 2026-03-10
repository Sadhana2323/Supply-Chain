import json
import os
import hashlib

DB_FILE = "users_db.json"

def _load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def _save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user(username):
    db = _load_db()
    return db.get(username)

def authenticate_user(username, password):
    user = get_user(username)
    if user and user["password_hash"] == _hash_password(password):
        return True
    return False

def create_user(username, password, email):
    db = _load_db()
    if username in db:
        return False
    
    db[username] = {
        "password_hash": _hash_password(password),
        "email": email,
        "onboarded": False,
        "company_data": {}
    }
    _save_db(db)
    return True

def save_company_data(username, data):
    db = _load_db()
    if username in db:
        db[username]["company_data"] = data
        db[username]["onboarded"] = True
        _save_db(db)
        return True
    return False
