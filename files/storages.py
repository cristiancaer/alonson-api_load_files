from django.core.files.storage import Storage
from django.conf import settings
from azure.storage.blob import BlobServiceClient, BlobClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta, timezone
from django.utils.deconstruct import deconstructible


@deconstructible  # to avid error:  Cannot serialize: <files.storages.AzureStorage object at makemigrations
class AzureStorage(Storage):
    def __str__(self) -> str:
        return 'AzureStorage'

    def get_service_sas_blob_token(self, blob_client: BlobClient):
        # Create a SAS token
        start_time = datetime.now(timezone.utc) - timedelta(minutes=1)
        expiry_time = start_time + timedelta(minutes=30)
        sas_token = 'error_sas_token'
        try:
            sas_token = generate_blob_sas(
                account_name=blob_client.account_name,
                container_name=blob_client.container_name,
                blob_name=blob_client.blob_name,
                account_key=blob_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=expiry_time,
                start=start_time
            )
        except Exception as e:
            pass
        return sas_token

    def __init__(self, base_url=None):
        self.ACCOUNT_URL = F"https://{settings.STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
        self.CONTAINER_NAME = settings.CONTAINER_NAME
        self.service_client = BlobServiceClient.from_connection_string(conn_str=settings.CONECTION_STRING)

    def _open(self, name, mode='rb'):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        handler = blob_client.download_blob()
        return handler

    def _save(self, name: str, memory_file_object):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        file = memory_file_object.file
        if blob_client.exists():
            blob_client.upload_blob(file, overwrite=True, metadata={'uploaded_filename': memory_file_object.name})
        else:
            blob_client.upload_blob(file, metadata={'uploaded_filename': memory_file_object.name})
        return name

    def delete(self, name):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        blob_client.delete_blob()

    def exists(self, name):
        # blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        return False  # do not check if file exists, overwrite it by default

    def url(self, name):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        token = self.get_service_sas_blob_token(blob_client)
        return f'{self.ACCOUNT_URL}/{self.CONTAINER_NAME}/{name}?{token}'
