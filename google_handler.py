# Google API test

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import io

SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveHandler():

	'''
	Initialize the GoogleDrive connection, build
	'''
	def __init__(self):
		try:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			self.creds = flow.run_local_server()
			self.service = build('drive', 'v3', credentials=self.creds)
		except Exception as e:
			print("> Error initializing GoogleDriveHandler.")
			print(e)

	'''
	Upload a file to GoogleDrive
	'''
	def upload_file(self, file_name, local_file_path):
		try:
			file_metadata = {'name': file_name}
			media = MediaFileUpload(local_file_path, mimetype='application/octet-stream')
			file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
			return file.get('id')
		except Exception as e:
			print("> Error uploading file to Google Drive.")
			print(e)
			return None

	'''
	Download a file from GoogleDrive
	'''
	def download_file(self, file_id, file_name):
		try:
			request = self.service.files().get_media(fileId=file_id)
			fh = io.FileIO(file_name, 'wb')
			downloader = MediaIoBaseDownload(fh, request)
			done = False
			while done == False:
			    status, done = downloader.next_chunk()
			    print("Download " + str(int(status.progress() * 100)) + "%.")
			return True
		except Exception as e:
			print("> Error downloading file from Google Drive.")
			print(e)
			return False

	'''
	Delete a file on GoogleDrive
	'''	
	def delete_file(self, file_id):
		try:
			self.service.files().delete(fileId=file_id).execute()
			return True
		except Exception as e:
			print("> Error deleting file from Google Drive.")
			print(e)
			return False
	'''
	Create new folder in GoogleDrive
	'''
	def create_new_folder(self, folder_name):
		try:
			folder_metadata = {
				'name': folder_name,
				'mimeType': 'application/vnd.google-apps.folder'
			}
			folder = self.service.files().create(body=folder_metadata, fields='id').execute()
			return folder.get('id')
		except Exception as e:
			print("> Error creating folder on Google Drive.")
			print(e)
			return None

# gd_handler = GoogleDriveHandler()
# file_id = gd_handler.upload_file("ee07a22a2938efcd83cf4abd4c412007.dms", "ee07a22a2938efcd83cf4abd4c412007.dms")
# print(gd_handler.download_file(file_id, "test.dms"))
# gd_handler.create_new_folder("helloworld")
# print(gd_handler.delete_file(file_id))

