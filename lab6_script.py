import requests
import hashlib
import os
import subprocess

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_msg = requests.get(file_url)

    if resp_msg.status_code == requests.codes.ok:
        file_content = resp_msg.text
        print(file_content)
        text = file_content.split(' ')[0]
        print(text)
         
    return text

def download_installer():
    vlc_link = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = requests.get(vlc_link)
    if resp_msg.status_code == requests.codes.ok:

     data = resp_msg.content
    return data

def installer_ok(installer_data, expected_sha256):
    vlc_hash = hashlib.sha256(installer_data).hexdigest()
    print(vlc_hash)
    if vlc_hash == expected_sha256:
        return True

def save_installer(installer_data):
    path = os.getenv('TEMP')
    vlc_path = os.path.join(path, 'vlc_setup.exe')
    with open(vlc_path, 'wb') as file:
        file.write(installer_data)
    return vlc_path

def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'], shell= True)
    return
    
def delete_installer(installer_path):
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()