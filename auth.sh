#!/bin/bash

# List all S3 buckets
buckets=$(aws s3api list-buckets --query 'Buckets[].Name' --output text)

for bucket in $buckets; do
  # Get the bucket ACL
  acl=$(aws s3api get-bucket-acl --bucket "$bucket" --output json)
  
  # Check if AuthenticatedUsers have READ permission
  readPermissions=$(echo $acl | jq -e '.Grants[] | select(.Grantee.URI=="http://acs.amazonaws.com/groups/global/AuthenticatedUsers" and (.Permission=="READ" or .Permission=="FULL_CONTROL"))')
  
  if [ $? -eq 0 ]; then
    echo "Bucket with AuthenticatedUsers READ permission found: $bucket"
  fi
done