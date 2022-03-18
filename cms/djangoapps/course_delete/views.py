import logging
from django.http import JsonResponse

from cms.djangoapps.contentstore.utils import delete_course as delete_course_and_groups
from opaque_keys.edx.keys import CourseKey
from xmodule.modulestore import ModuleStoreEnum
from common.djangoapps.student.models import CourseEnrollment

log = logging.getLogger("course_delete")


def delete_course(request):
    """
    Delete course from platform.
    """
    course_id = request.POST.get('course_id', '')
    try:
        course_key = CourseKey.from_string(course_id)
        delete_course_and_groups(course_key, ModuleStoreEnum.UserID.mgmt_command)
        CourseEnrollment.objects.filter(course_id=course_key).delete()
        return JsonResponse(status=200, data={})
    except Exception as error:
        log.error("Error while deleting course. The error message is:{}".format(str(error)))
        return JsonResponse(status=400, data={
            'error_message': str(error)
        })
