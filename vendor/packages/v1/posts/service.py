import os
import urllib.parse
import hashlib
import time
import boto3
from pathlib import Path
from .repository import PostRepository


class PostService:
    def __init__(self):
        self.repo = PostRepository()
        # Initialize S3 client - AWS Lambda provides credentials automatically
        self.s3_client = boto3.client("s3")
        self.bucket_name = "aws-petcare-image"

    def get_posts(
        self,
        user_id: int = None,
        category_id: int = None,
        status_id: int = None,
        title: str = None,
        page: int = 1,
        limit: int = 10,
    ):
        return self.repo.get_posts(user_id, category_id, status_id, title, page, limit)

    def get_post(self, post_id: int):
        return self.repo.get_post(post_id)

    def get_posts_paginated(self, page: int = 1, limit: int = 10):
        return self.repo.get_posts_paginated(page, limit)

    def get_total_posts(self):
        return self.repo.get_total_posts()

    def create_post(self, post: dict):
        return self.repo.create_post(post)

    def upload_image(self, image_url: str):
        """
        Extract image name from image_url and create a unique path for storing in AWS S3 bucket aws-petcare-image/posts/

        Args:
            image_url (str): The original image URL or local file path

        Returns:
            str: The new S3 path for storing the image (e.g., "aws-petcare-image/posts/abc123_filename.jpg")
        """
        if not image_url:
            return None

        # Check if it's a local file path (contains backslashes or forward slashes)
        if "\\" in image_url or "/" in image_url:
            # Handle local file path
            # Normalize path separators
            normalized_path = image_url.replace("\\", "/")
            # Get the filename from the path
            original_filename = os.path.basename(normalized_path)
        else:
            # Handle URL
            parsed_url = urllib.parse.urlparse(image_url)
            original_filename = os.path.basename(parsed_url.path)

            # If no filename found in path, try to get it from query parameters
            if not original_filename or original_filename == "":
                query_params = urllib.parse.parse_qs(parsed_url.query)
                if "filename" in query_params:
                    original_filename = query_params["filename"][0]
                else:
                    # Generate a default filename with timestamp
                    original_filename = f"image_{int(time.time())}.jpg"

        # If still no filename, generate one
        if not original_filename or original_filename == "":
            original_filename = f"image_{int(time.time())}.jpg"

        # Generate unique hash for the filename
        # Combine original filename, timestamp, and some randomness for uniqueness
        unique_string = f"{original_filename}_{int(time.time() * 1000)}"
        hash_object = hashlib.md5(unique_string.encode())
        hash_hex = hash_object.hexdigest()[:8]  # Take first 8 characters of hash

        # Get file extension
        file_name, file_extension = os.path.splitext(original_filename)
        if not file_extension:
            file_extension = ".jpg"  # Default extension

        # Create unique filename with hash
        unique_filename = f"{hash_hex}_{file_name}{file_extension}"

        # Create the S3 target path
        target_path = f"posts/{unique_filename}"

        return target_path

    def upload_file_to_s3(self, file_content, filename):
        """
        Upload a file directly to AWS S3

        Args:
            file_content: The file content (bytes or file-like object)
            filename: The filename to use in S3

        Returns:
            str: The S3 URL of the uploaded file
        """
        try:
            # Generate unique S3 key
            s3_key = self.upload_image(filename)
            if not s3_key:
                return None

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType="image/jpeg",  # Adjust based on file type
            )

            # Return the S3 URL
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            return s3_url

        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return None

    def update_post(self, post_id: int, post: dict):
        return self.repo.update_post(post_id, post)

    def delete_post(self, post_id: int):
        post = self.get_post(post_id)
        if post is None:
            raise ValueError("Post not found")
        return self.repo.delete_post(post_id)
