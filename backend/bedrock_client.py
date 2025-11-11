import logging
import boto3
from botocore.config import Config
import os

from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockClient:
    """Implementation of BedrockClient to interact with Bedrock Claude service."""
    
    log: logging.Logger = logging.getLogger("BedrockClient")
    
    def __init__(self, aws_access_key: Optional[str] = None, aws_secret_key: Optional[str] = None,
                 assumed_role: Optional[str] = None, region_name: Optional[str] = "us-east-1") -> None:
        self.region_name = region_name
        self.assumed_role = assumed_role
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
    
    def _get_bedrock_client(
            self,
            runtime: Optional[bool] = True,
    ):
        """Create a boto3 client for Amazon Bedrock, with optional configuration overrides."""
        if self.region_name is None:
            target_region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
        else:
            target_region = self.region_name
        session_kwargs = {"region_name": target_region}
        client_kwargs = {**session_kwargs}
        
        profile_name = os.environ.get("AWS_PROFILE")
        
        if profile_name:
            session_kwargs["profile_name"] = profile_name
        
        retry_config = Config(
            region_name=target_region,
            retries={
                "max_attempts": 10,
                "mode": "standard",
            },
        )
        session = boto3.Session(**session_kwargs)
        
        if self.assumed_role:
            sts = session.client("sts")
            response = sts.assume_role(
                RoleArn=str(self.assumed_role),
                RoleSessionName="bedrock-admin"
            )
            client_kwargs["aws_access_key_id"] = response["Credentials"]["AccessKeyId"]
            client_kwargs["aws_secret_access_key"] = response["Credentials"]["SecretAccessKey"]
            client_kwargs["aws_session_token"] = response["Credentials"]["SessionToken"]
        
        if self.aws_access_key and self.aws_secret_key:
            client_kwargs["aws_access_key_id"] = self.aws_access_key
            client_kwargs["aws_secret_access_key"] = self.aws_secret_key
        
        service_name = 'bedrock-runtime' if runtime else 'bedrock'
        
        bedrock_client = session.client(
            service_name=service_name,
            config=retry_config,
            **client_kwargs
        )
    
        return bedrock_client
    
    def _close_bedrock(self):
        """Close Bedrock client."""
        if hasattr(self, 'bedrock') and self.bedrock:
            self.bedrock.close()
    
    def __del__(self):
        """Destructor."""
        self._close_bedrock()