import secrets
import string

def generate_client_id(length=24):
    """Generate a random client ID."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_client_secret(length=48):
    """Generate a random client secret."""
    alphabet = string.ascii_letters + string.digits + '-._~'
    return ''.join(secrets.choice(alphabet) for _ in range(length))