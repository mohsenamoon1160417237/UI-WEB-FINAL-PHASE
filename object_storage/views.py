from botocore.exceptions import ClientError

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from utils.arvan_authenticate import arvan_auth
from .models import UserObjectStorage


@login_required
def upload_object(request):
    if request.method == "POST":
        user = request.user
        s3_resource = arvan_auth()
        if not s3_resource:
            return
        try:
            bucket = s3_resource.Bucket('mohsenamoon1380')
            file_path = request.FILES['fileInput'].file.name
            object_name = request.FILES['fileInput'].name

            with open(file_path, "rb") as file:
                bucket.put_object(
                    ACL='private',
                    Body=file,
                    Key=object_name
                )
                UserObjectStorage.objects.create(
                    file_name=object_name,
                    file_size=request.FILES['fileInput'].size,
                    user=user
                )
        except ClientError as e:
            print(f"Arvan client Error: {e}")

        return redirect("home")


@login_required
def delete_object(request, file_id: int):
    if request.method == "POST":
        file = UserObjectStorage.objects.get(id=file_id)
        try:
            s3_resource = arvan_auth()
            bucket = s3_resource.Bucket('mohsenamoon1380')
            obj = bucket.Object(file.file_name)

            response = obj.delete(
                VersionId='',
            )
            file.delete()
        except ClientError as e:
            print(f"error while deleting object: {e}")

        return redirect("home")


@login_required
def download_object(request, file_id: int):
    if request.method == "POST":
        file = UserObjectStorage.objects.get(id=file_id)
        try:
            s3_resource = arvan_auth()
            bucket = s3_resource.Bucket('mohsenamoon1380')
            download_path = f'/Users/mohsenamoon/Downloads/{file.file_name}'

            bucket.download_file(
                file.file_name,
                download_path
            )
        except ClientError as e:
            print(f"error while deleting object: {e}")

        return redirect("home")
