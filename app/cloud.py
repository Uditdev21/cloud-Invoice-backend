import cloudinary
import cloudinary.uploader
import cloudinary.api

# Initialize Cloudinary with your credentials
cloudinary.config(
    cloud_name='dnkghgh1q',   # Replace with your Cloudinary cloud name
    api_key='912783413358286',  # Replace with your Cloudinary API key
    api_secret='jjjzu6H0bbpyN6YPNBbTsM0mXLc',  # Replace with your Cloudinary API secret
    secure=True  # Use HTTPS for secure connection
)

def upload_file(file_path: str):
    """Uploads a single file to Cloudinary and returns the file URL."""
    try:
        response = cloudinary.uploader.upload(file_path, folder="invoices", resource_type="raw")
        # You can access the URL of the uploaded file from the response
        print("File uploaded successfully!")
        print("File URL:", response['secure_url'])
        return response['secure_url']
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

# Example usage: Upload a file located at 'path/to/your/file.jpg'

