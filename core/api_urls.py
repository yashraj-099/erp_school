from rest_framework.routers import DefaultRouter
from . import api_views
from django.urls import path, include
router = DefaultRouter()
router.register('students', api_views.StudentViewSet)
router.register('teachers', api_views.TeacherViewSet)
router.register('subjects', api_views.SubjectViewSet)
router.register('fees', api_views.FeeRecordViewSet)
router.register('events', api_views.EventViewSet)
router.register('schools', api_views.SchoolViewSet)
urlpatterns = [path('', include(router.urls)),]
