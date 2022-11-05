#!/bin/bash

docker volume create --label s3 hardml_s3 || true

docker run -d --rm \
           -v hardml_s3:/data \
           -p 9900:9000 \
           -p 9901:9001 \
           -e MINIO_ACCESS_KEY=s3_access_key \
           -e MINIO_SECRET_KEY=s3_secret_key \
           --name minio_hardml \
           minio/minio:RELEASE.2022-10-29T06-21-33Z \
           server --console-address :9001 /data
