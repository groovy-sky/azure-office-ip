from azure.storage.blob import BlobServiceClient,ContentSettings
import requests
import json
import os
from datetime import datetime
import uuid
import azure.functions as func

class EndpointsClient:
  def __init__(self, storage_connection_string, storage_container_name, working_path):
    service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    self.client = service_client.get_container_client(storage_container_name)
    self.uuid = str(uuid.uuid4())
    self.container_name = storage_container_name
    self.main_page = 'main.html'
    self.out_path = 'artifacts'
    self.artifacts_path = working_path + '/' + self.out_path
    if not os.path.exists(self.artifacts_path):
      os.mkdir(self.artifacts_path)
    self.clear()
  def clear(self):
    self.sorted_ip_list = {}
    self.ip_list = None
  def get_o365_endpoints(self):
    '''
    Get Office 365 endpoints IP addresses
    '''
    if self.ip_list != None:
        self.clear()
    office_response = requests.get("https://endpoints.office.com/endpoints/worldwide?clientrequestid={}".format(self.uuid))
    self.ip_list = office_response.json()
    for item in self.ip_list:
        if item.get('ips') != None:
            ip_list = item['ips']
        else:
            ip_list = False
        if item['serviceAreaDisplayName'] not in self.sorted_ip_list and ip_list:
            self.sorted_ip_list[item['serviceAreaDisplayName']] = ip_list
        elif ip_list:
            self.sorted_ip_list[item['serviceAreaDisplayName']].extend(ip_list)
  def export_locally(self):
    for key in self.sorted_ip_list.keys():
        with open(f"{self.artifacts_path}/{key}.txt", 'w') as out_file:
            for item in self.sorted_ip_list[key]:
                out_file.write("%s\n" % item)
  def new_main_page(self):
      artifacts_files = os.listdir(self.artifacts_path)
      main_page_content = '<html>\n<head>\n</head>\n<body>\n Generated date:<br>' + str(datetime.now()) + '<br><br>Generated list:<br>'
      for item in artifacts_files:
        main_page_content = main_page_content + '<a href="' + self.out_path + '/' + item + '" download>' + item + '</href>\n <br>'
      main_page_content += '</body></html>'
      with open(self.main_page,'w') as out_file:
          out_file.write("%s" % main_page_content)
      self.upload_file(self.main_page,self.main_page)
  def upload(self, source, dest):
    '''
    Upload a file or directory to a path inside the container
    '''
    if (os.path.isdir(source)):
      self.upload_dir(source, dest)
    else:
      self.upload_file(source, dest)
  def upload_file(self, source, dest):
    '''
    Upload a single file to a path inside the container
    '''
    content_settings=ContentSettings(content_type='text/html')
    print(f'Uploading {source} to {dest}')
    with open(source, 'rb') as data:
      self.client.upload_blob(name=dest, data=data, content_settings=content_settings, overwrite=True)
  def upload_dir(self, source='', dest=''):
    '''
    Upload a directory to a path inside the container
    '''
    if not source:
        source = self.artifacts_path
    prefix = '' if dest == '' else dest + '/'
    prefix += os.path.basename(source) + '/'
    for root, dirs, files in os.walk(source):
      for name in files:
        dir_part = os.path.relpath(root, source)
        dir_part = '' if dir_part == '.' else dir_part + '/'
        file_path = os.path.join(root, name)
        blob_path = prefix + dir_part + name
        self.upload_file(file_path, blob_path)
  def download(self, source, dest):
    '''
    Download a file or directory to a path on the local filesystem
    '''
    if not dest:
      raise Exception('A destination must be provided')
    blobs = self.ls_files(source, recursive=True)
    if blobs:
      # if source is a directory, dest must also be a directory
      if not source == '' and not source.endswith('/'):
        source += '/'
      if not dest.endswith('/'):
        dest += '/'
      # append the directory name from source to the destination
      dest += os.path.basename(os.path.normpath(source)) + '/'
      blobs = [source + blob for blob in blobs]
      for blob in blobs:
        blob_dest = dest + os.path.relpath(blob, source)
        self.download_file(blob, blob_dest)
    else:
      self.download_file(source, dest)
  def download_file(self, source, dest):
    '''
    Download a single file to a path on the local filesystem
    '''
    # dest is a directory if ending with '/' or '.', otherwise it's a file
    if dest.endswith('.'):
      dest += '/'
    blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest
    print(f'Downloading {source} to {blob_dest}')
    os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
    bc = self.client.get_blob_client(blob=source)
    with open(blob_dest, 'wb') as file:
      data = bc.download_blob()
      file.write(data.readall())
  def ls_files(self, path, recursive=False):
    '''
    List files under a path, optionally recursively
    '''
    if not path == '' and not path.endswith('/'):
      path += '/'
    blob_iter = self.client.list_blobs(name_starts_with=path)
    files = []
    for blob in blob_iter:
      relative_path = os.path.relpath(blob.name, path)
      if recursive or not '/' in relative_path:
        files.append(relative_path)
    return files

def main(mytimer: func.TimerRequest) -> None:
  client = EndpointsClient(storage_connection_string=os.environ['AZURE_STORAGE_CONNECTION_STRING'], storage_container_name='$web',working_path='/tmp')
  client.get_o365_endpoints()
  client.export_locally()
  client.upload_dir()
  client.new_main_page()