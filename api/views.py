import logging
import os
from http import HTTPStatus

from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import TestFilePath
from api.models import TestRunRequest
from api.serializers import TestRunRequestSerializer, TestRunRequestItemSerializer
from api.tasks import execute_test_run_request
from api.usecases import get_assets


logger = logging.getLogger(__name__)

class TestRunRequestAPIView(ListCreateAPIView):
    serializer_class = TestRunRequestSerializer
    queryset = TestRunRequest.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        instance = serializer.save()
        execute_test_run_request.delay(instance.id)

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['test_file']
        directory = request.data['upload_dir']  # "form" data

        file_name = default_storage.save(file_obj.name, file_obj)
        logger.info(file_name)

        file_record = TestFilePath()
        # make up some path using the directory,
        # doing this whole thing better requires a decent model refactor:
        file_record.path = os.path.join(
            settings.MEDIA_ROOT,
            directory,
            file_name
        )
        file_record.directory = directory
        file_record.is_user_upload = True
        file_record.save()

        return Response(status=HTTPStatus.CREATED)


class TestRunRequestItemAPIView(RetrieveAPIView):
    serializer_class = TestRunRequestItemSerializer
    queryset = TestRunRequest.objects.all()
    lookup_field = 'pk'


class AssetsAPIView(APIView):

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data=get_assets())
