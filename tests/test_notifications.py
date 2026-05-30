import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.auth import generate_email_verification_token

# Create a test client for the FastAPI application
client = TestClient(app)

def test_generate_email_verification_token():
    """
    Tests the generation of an email verification token.
    
    This test checks if the function generates a valid JWT token with the correct user ID
    and if it expires within the expected time frame.
    """
    user_id = 12345
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    
    # Generate the token
    encoded_jwt = generate_email_verification_token(user_id)
    
    # Decode the token to check its contents and expiration time
    try:
        payload = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload.get("user_id") == user_id
        assert datetime.fromtimestamp(payload["exp"]) == expire
    except JWTError:
        pytest.fail("Failed to decode the token")

if __name__ == "__main__":
    pytest.main()