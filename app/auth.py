from typing import Optional
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import bcrypt
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()
secret = os.getenv("SECRET_KEY")
Algorithm=os.getenv("ALGORITHM")

# Secrets should ideally be stored in environment variables for security
SECRET_KEY =secret  # Replace with your actual secret key
ALGORITHM = Algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class PasswordAuth:
    """Password authentication utilities for hashing and verifying passwords."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain-text password with a generated salt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a hashed password."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class JwtToken:
    """JWT utilities for authentication"""

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Creation of access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_and_decode_jwt(token: str=Depends(oauth2_scheme)) -> dict:
        """Verify and decode the JWT token for the user."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decode the token and extract the payload
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # email: str = payload.get("Email")

            # if email is None:
            #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide a valid email in the token")

            # You can add further verification logic to check the existence of the user in the database


            # Return the decoded token payload
            return payload
        except JWTError:
            # Handle any JWT decoding errors
            raise credentials_exception
        except Exception as e:
            # Log unexpected errors and re-raise as a 500 Internal Server Error
            print(f"Error during JWT verification: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while verifying the token.",
            )
