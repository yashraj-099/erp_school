- Add role-based access control to views in core/views.py
  - Admin only: admin_dashboard, students_list, students_create, students_update, students_delete, teachers_list, teachers_create, teachers_update, teachers_delete, subjects_list, subjects_create, subjects_update, subjects_delete, fees_list, fees_create, fees_update, fees_delete, events_list, events_create, events_update, events_delete, schools_list, schools_create, schools_update, schools_delete
  - Teacher: teacher_dashboard, subjects_list, subjects_create, subjects_update, subjects_delete, events_list, events_create, events_update, events_delete
  - Student: student_dashboard, fees_list, events_list
  - All logged in: select_dashboard, redirect_dashboard, logout_view
- Test login as newadmin (superuser), teacher, student

Role-based access control implementation steps:
1. ✅ Add @role_required('Admin') to admin_dashboard
2. ✅ Add @role_required('Admin') to students_list, students_create, students_update, students_delete
3. ✅ Add @role_required('Admin') to teachers_list, teachers_create, teachers_update, teachers_delete
4. ✅ Add @role_required('Admin', 'Teacher') to subjects_list, subjects_create, subjects_update, subjects_delete
5. ✅ Add @role_required('Admin') to fees_list, fees_create, fees_update, fees_delete
6. ✅ Add @role_required('Admin', 'Teacher', 'Student') to events_list, events_create, events_update, events_delete
7. ✅ Add @role_required('Admin') to schools_list, schools_create, schools_update, schools_delete
8. ✅ Add @role_required('Teacher') to teacher_dashboard
9. ✅ Add @role_required('Student') to student_dashboard
10. ✅ Remove the unrelated login_redirect function at the end of views.py
11. ✅ Test the application by running python manage.py runserver and checking access for different roles
