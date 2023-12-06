from django.core.files.storage import Storage
from django.conf import settings
from azure.storage.blob import BlobServiceClient, BlobClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta, timezone


class AzureStorage(Storage):
    def get_service_sas_blob_token(self, blob_client: BlobClient):
        # Create a SAS token that's valid for one day, as an example
        start_time = datetime.now(timezone.utc)
        expiry_time = start_time + timedelta(minutes=1)
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
        return open(blob_client, mode)

    def _save(self, name, memory_file_object):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        file = memory_file_object.file
        blob_client.upload_blob(file)
        return name

    def delete(self, name):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        blob_client.delete_blob()

    def exists(self, name):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        return blob_client.exists()

    def url(self, name):
        blob_client = self.service_client.get_blob_client(container=self.CONTAINER_NAME, blob=name)
        token = self.get_service_sas_blob_token(blob_client)
        return f'{self.ACCOUNT_URL}/{self.CONTAINER_NAME}/{name}?{token}'
