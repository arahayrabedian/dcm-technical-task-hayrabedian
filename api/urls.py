from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from .views import TestRunRequestAPIView, TestRunRequestItemAPIView, AssetsAPIView, FileUploadView

urlpatterns = [
    path('assets', AssetsAPIView.as_view(), name='assets'),
    path('test-run', TestRunRequestAPIView.as_view(), name='test_run_req'),
    path('test-file', FileUploadView.as_view(), name='add_test_file'),
    path('test-run/<pk>', TestRunRequestItemAPIView.as_view(), name='test_run_req_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # not a production way of doing things.

