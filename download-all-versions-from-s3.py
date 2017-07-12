import os
import boto3
from boto3.s3.transfer import S3Transfer

bucket = 'BUCKET'
key = 'KEY'
s3 = boto3.resource('s3')
bucket_contents = s3.Bucket(bucket)
client = boto3.client('s3')
transfer = S3Transfer(client)

for file in bucket_contents.objects.all():
   if file.key.startswith(key):
      versions = s3.Bucket(bucket).object_versions.filter(Prefix=file.key)

      count = 0;

      for version in versions:
         obj = version.get()
 
         sourcepath  = file.key.split("/")
         targetpath = ''

         for i in range(0,len(sourcepath)-1):
           targetpath = targetpath + sourcepath[i] + "/"  
           
           if not os.path.exists(targetpath):
              os.makedirs(targetpath) 
            
         transfer.download_file(bucket, file.key, file.key + "_" + str(count) + ".json", extra_args={'VersionId': obj['VersionId'] })

         count+=1
