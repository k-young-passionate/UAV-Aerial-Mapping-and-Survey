import requests, sys, os, glob, json, time
import status_codes

# API Example Requirements:
#   >15 Images
#   >60% Image Overlap
#   Valid Imagery .ZIP File URL
#   EXIF Metadata (GPS Lat, GPS Lon, GPS Elevation, Focal Length, etc)
#   webhook GET request "Optional"

zipurl = "http://dronemapper.com/examples/nir-test.zip"
webhook = "https://webhook.site/8ff5306f-8e25-4788-b4cd-204ca14c55dc"
task_name = "DJI NIR Phantom 3 Advanced"

res = requests.post('https://dronemapper.io/api/token-auth/',
                    data={'username': 'API-USERNAME',
                          'password': 'API-PASSWORD'}).json()

if 'token' in res:
    print("[*] Got DroneMapper API Token")
    token = res['token']

    res = requests.post('https://dronemapper.io/api/projects/',
                        headers={'Authorization': 'JWT {}'.format(token)},
                        data={'name': 'API Project'}).json()
    if 'id' in res:
        print("[*] New Project Created: \n\t{}".format(res)) 
        project_id = res['id']

        options = json.dumps([
            {'name': "zipurl", 'value': zipurl},
            {'name': "webhook", 'value': webhook}
        ])
        res = requests.post('https://dronemapper.io/api/projects/{}/tasks/'.format(project_id),
                    headers={'Authorization': 'JWT {}'.format(token)},
                    data={
                        'options': options,
                        'zipurl': zipurl,
                        'webhook': webhook,
                        'name': task_name
                    }).json()

        print("[*] New Task Created: \n\t{}".format(res))
        task_id = res['id']

        while True:
            time.sleep(3)
            res = requests.get('https://dronemapper.io/api/projects/{}/tasks/{}/'.format(project_id, task_id),
                        headers={'Authorization': 'JWT {}'.format(token)}).json()
            
            if res['status'] == status_codes.COMPLETED:
                print("\n[*] Task Complete")
                break
            elif res['status'] == status_codes.FAILED:
                print("[*] Task Failed: {}".format(res))

                # Delete Project (Including Tasks)
                print("[*] Clean Up")
                requests.delete("https://dronemapper.io/api/projects/{}/".format(project_id),
                    headers={'Authorization': 'JWT {}'.format(token)})
                sys.exit(1)
            else:
                seconds = res['processing_time'] / 1000
                if seconds < 0: 
                    seconds = 0
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                sys.stdout.write("\r[!] Processing... [%02d:%02d:%02d]" % (h, m, s))
                sys.stdout.flush()

        # Orthomosaic
        res = requests.get("https://dronemapper.io/api/projects/{}/tasks/{}/download/orthophoto.tif".format(project_id, task_id),
                        headers={'Authorization': 'JWT {}'.format(token)},
                        stream=True)
        with open("ORT-DrnMppr.tif", 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        print("[*] Wrote ./ORT-DrnMppr.tif")

        # Digital Elevation Model
        res = requests.get("https://dronemapper.io/api/projects/{}/tasks/{}/download/dsm.tif".format(project_id, task_id),
                        headers={'Authorization': 'JWT {}'.format(token)},
                        stream=True)
        with open("DEM-DrnMppr.tif", 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        print("[*] Wrote ./DEM-DrnMppr.tif")

        # Point Cloud
        res = requests.get("https://dronemapper.io/api/projects/{}/tasks/{}/download/pointcloud.ply".format(project_id, task_id),
                        headers={'Authorization': 'JWT {}'.format(token)},
                        stream=True)
        with open("PLY-DrnMppr.ply", 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
        print("[*] Wrote ./PLY-DrnMppr.ply")        

        # Delete Project (Including Tasks)
        print("[*] Clean Up")
        requests.delete("https://dronemapper.io/api/projects/{}/".format(project_id),
                        headers={'Authorization': 'JWT {}'.format(token)})
    else:
        print("[*] Cannot Create Project: {}".format(res))
else:
    print("[*] Invalid API Credentials!")
