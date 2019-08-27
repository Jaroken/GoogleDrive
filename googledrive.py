from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime
import os
rootfolder = "<folder on computer>"
path = str(datetime.date.today()) # if creating a folder each day

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(rootfolder+path):
    for file in f:
        files.append(file)
        
gauth = GoogleAuth() #fyi - need a client_secrets.json saved in directory where this is being run - obtain from googledeveloper site

# Try to load saved client credentials
try:
    gauth.LoadCredentialsFile("mycreds.txt")
except:
    # Run to get credentials saved
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

# Create folder.
folder_metadata = {
    'title' : str(datetime.date.today()),
    # The mimetype defines this new file as a folder, so don't change this.
    'mimeType' : 'application/vnd.google-apps.folder', 
    'parents':[{'id':'<google drive folder id from url>'}]
}
folder = drive.CreateFile(folder_metadata)
folder.Upload()

for i in files:
    file1 = drive.CreateFile({"parents":  [{"kind": "drive#fileLink","id": folder['id']}]})
    file1.SetContentFile(rootfolder+path+'\\'+i)
    file1.Upload()
