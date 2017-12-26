import dropbox;
import os;
import schedule;
import json;


data = json.loads(open('dropboxKey.json').read())

dbx = dropbox.Dropbox(data["DropBox_Api_Key"]);
dbx.users_get_current_account();

def uploadToDropbox():
    if not os.listdir("/mnt/c/dev/song-uploader/songs"):
        print("no songs found ..");
        return;
    for filename in os.listdir("/mnt/c/dev/song-uploader/songs"):
        print "Uploading " + filename
        f = open("/mnt/c/dev/song-uploader/songs/"+filename,"rb");
        dbx.files_upload(bytes(f.read()), '/music/'+filename);
        f.close();
        print "File uploaded"
        os.remove("/mnt/c/dev/song-uploader/songs/"+filename);
        print  filename + " is removed locally"


