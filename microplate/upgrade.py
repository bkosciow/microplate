import json
import os
import urequests
import uhashlib
import gc
import machine


filename = "/.upgrade.json"
temp_dir = "tmp_upgrade"

def get_params():
    with open(filename, 'r') as f:
        params = json.load(f)

    if "base_url" not in params or "files" not in params or "type" not in params:
        print("data missing")
        params = None

    return params


def ensure_tmp_dir_exists(temp_dir):
    if temp_dir not in os.listdir():
        os.mkdir(temp_dir)
        print(f"Created directory: {temp_dir}")
        return True

    files = os.listdir(temp_dir)
    if len(files) == 0:
        print(f"Directory {temp_dir} exists and is empty")
        return True

    for _file in files:
        file_path = f"{temp_dir}/{_file}"
        os.remove(file_path)
    print(f"Directory {temp_dir} is now empty")
    return True


def download_file(url, filename):
    chunk_size = 512
    try:
        gc.collect()
        print(f"Starting download from {url}")
        response = urequests.get(url, timeout=30)
        if response.status_code == 200:
            print("Download started...")

            # Open file for writing
            with open(filename, 'wb') as f:
                downloaded = 0
                while True:
                    chunk = response.raw.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if downloaded % (chunk_size * 10) == 0:
                        gc.collect()

            print(f"Download completed! {downloaded} bytes")
            response.close()
            return True
        else:
            print(f"HTTP Error: {response.status_code}")
            response.close()
            return False
    except Exception as e:
        print(f"Error downloading file: {e}")
        gc.collect()
        return False

params = get_params()
# print(params)
ensure_tmp_dir_exists(temp_dir)
base_url = params['base_url']
# os.remove(filename)
crc_ok = True
for file in params['files']:
    url = base_url +"/get/"+  file
    filepath = temp_dir +"/" + file
    print(f"Getting {url} to {filepath}")
    if download_file(url, filepath):
        with open(filepath, 'rb') as f:
            hasher = uhashlib.sha256()
            while True:
                chunk = f.read(512)
                if not chunk:
                    break
                hasher.update(chunk)
            file_hash = hasher.digest().hex()
        url = base_url + "/validate/" + file
        response = urequests.post(url, timeout=30, json={"hash": file_hash})
        if response.status_code != 200:
            print(response.content, file_hash)
            print("HASH FAILED - UPGRADE ABORTED")
            crc_ok = False
            break
    else:
        print("DOWNLOAD FAILED - UPGRADE ABORTED")
        crc_ok = False
        break

if crc_ok:
    target = None
    if params['type'] == "userspace":
        print("Files OK - replacing userspace files")
        target = "/"

    if params['type'] == "microplate":
        print("Files OK - replacing microplate files")
        target = "/microplate/"

    for file in params['files']:
        source = filepath = temp_dir +"/" + file
        destination = target + file
        print(f"Replacing {destination} with {source}")

        try:
            os.rename(source, destination)
            print("OK")
        except OSError as e:
            print(f"Error moving {file}: {e}")

os.remove(filename)
print("Rebooting the device")
machine.reset()
