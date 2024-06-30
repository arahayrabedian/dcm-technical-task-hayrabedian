from api.models import TestFilePath, TestEnvironment
from api.serializers import TestFilePathSerializer, TestEnvironmentSerializer


def get_assets():
    return {
        'available_paths': TestFilePathSerializer(TestFilePath.objects.all().order_by('path'), many=True).data,
        'upload_dirs': [record[0] for record in TestFilePath.objects.order_by().values_list('directory').distinct()],
        'test_envs': TestEnvironmentSerializer(TestEnvironment.objects.all().order_by('name'), many=True).data,
    }
