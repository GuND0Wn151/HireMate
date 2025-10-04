import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException
from app.core.config import settings
import uuid
from datetime import datetime
import os
from typing import Optional

class S3Service:
    def __init__(self):
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.bucket_name = settings.S3_BUCKET_NAME
        except NoCredentialsError:
            raise HTTPException(
                status_code=500, 
                detail="AWS credentials not found. Please configure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
            )

    async def upload_pdf(self, file_content: bytes, original_filename: str, user_email: Optional[str] = None) -> dict:
        """
        Upload a PDF file to S3 bucket with user email folder organization
        
        Args:
            file_content: The file content as bytes
            original_filename: The original filename of the uploaded file
            user_email: User email for organizing files in folders (uses part before @)
            
        Returns:
            dict: Contains file_url, s3_key, and metadata
        """
        try:
            # Generate unique filename with timestamp and UUID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_extension = os.path.splitext(original_filename)[1].lower()
            
            # Validate file extension
            if file_extension != '.pdf':
                raise HTTPException(
                    status_code=400, 
                    detail="Only PDF files are allowed"
                )
            
            # Validate user_email is provided
            if not user_email:
                raise HTTPException(
                    status_code=400, 
                    detail="User email is required for file organization"
                )
            
            # Extract email prefix (part before @)
            try:
                email_prefix = user_email.split('@')[0]
                if not email_prefix:
                    raise ValueError("Invalid email format")
            except (IndexError, ValueError):
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid email format. Please provide a valid email address"
                )
            
            # Check if the user folder exists, if not it will be created automatically
            await self._ensure_user_folder_exists(email_prefix)
            
            # Create S3 key with simple email_prefix/filename structure
            s3_key = f"{email_prefix}/{original_filename}"
            
            # Upload file to S3 (ACLs disabled, using bucket policy for public access)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType='application/pdf',
                Metadata={
                    'original_filename': original_filename,
                    'upload_timestamp': timestamp,
                    'user_email': user_email,
                    'email_prefix': email_prefix
                }
            )
            
            # Generate pre-signed URL for secure access (expires in 7 days)
            file_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=604800  # 7 days in seconds
            )
            
            return {
                "file_url": file_url,
                "s3_key": s3_key,
                "original_filename": original_filename,
                "file_size": len(file_content),
                "upload_timestamp": timestamp,
                "user_email": user_email,
                "email_prefix": email_prefix
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise HTTPException(
                    status_code=500,
                    detail=f"S3 bucket '{self.bucket_name}' does not exist"
                )
            elif error_code == 'AccessDenied':
                raise HTTPException(
                    status_code=500,
                    detail="Access denied to S3 bucket. Check your AWS permissions"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to upload file to S3: {str(e)}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error during file upload: {str(e)}"
            )

    async def _ensure_user_folder_exists(self, email_prefix: str) -> bool:
        """
        Check if user folder exists in S3, create a placeholder if it doesn't
        
        Args:
            email_prefix: The email prefix (part before @) to check/create folder for
            
        Returns:
            bool: True if folder exists or was created successfully
        """
        try:
            # Check if user folder exists by listing objects with the email prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"{email_prefix}/",
                MaxKeys=1
            )
            
            # If no objects found with this prefix, folder doesn't exist
            if not response.get('Contents'):
                # Create a placeholder file to establish the folder structure
                placeholder_key = f"{email_prefix}/.folder_placeholder"
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=placeholder_key,
                    Body=b"",
                    ContentType='text/plain',
                    Metadata={
                        'purpose': 'folder_placeholder',
                        'email_prefix': email_prefix,
                        'created_at': datetime.now().isoformat()
                    }
                )
                print(f"Created user folder for email prefix: {email_prefix}")
            else:
                print(f"User folder already exists for email prefix: {email_prefix}")
            
            return True
            
        except ClientError as e:
            print(f"Error checking/creating user folder for {email_prefix}: {str(e)}")
            return False

    async def delete_file(self, s3_key: str) -> bool:
        """
        Delete a file from S3 bucket
        
        Args:
            s3_key: The S3 key of the file to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file from S3: {str(e)}"
            )

    async def get_file_info(self, s3_key: str) -> dict:
        """
        Get information about a file in S3
        
        Args:
            s3_key: The S3 key of the file
            
        Returns:
            dict: File metadata and information
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            return {
                "s3_key": s3_key,
                "file_size": response['ContentLength'],
                "last_modified": response['LastModified'],
                "content_type": response.get('ContentType', 'unknown'),
                "metadata": response.get('Metadata', {})
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise HTTPException(
                    status_code=404,
                    detail="File not found in S3"
                )
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get file info from S3: {str(e)}"
            )

# Create a global instance
s3_service = S3Service()
