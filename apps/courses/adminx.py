# -*- coding:utf-8 -*-
__author__ = 'dapeng'
__date__ = '18-10-11 上午9:18'

import xadmin

from .models import Course, CourseResource, Lesson, Video, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0

class CourseAdmin(object):
    list_display = ['course_org', 'name', 'desc', 'detail', 'is_banner', 'degree', 'learn_times', 'students', 'get_zj_nums', 'favor_nums', 'click_nums', 'add_time']
    search_fields = ['course_org', 'name', 'desc', 'detail', 'degree', 'students', 'favor_nums', 'click_nums']
    list_filter = ['course_org', 'name', 'desc', 'detail', 'is_banner', 'degree', 'learn_times', 'students', 'favor_nums', 'click_nums', 'add_time']
    model_icon = 'fa fa-book'
    readonly_fields = ['click_nums', 'favor_nums', 'students']
    relfield_style = 'fk-ajax'
    list_editable = ['degree', 'detail']
    inlines = [LessonInline, CourseResourceInline]
    exclude = ['favor_nums']
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # save_models在xadmin/views/edit.py中
    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)

class BannerCourseAdmin(object):
    list_display = ['course_org', 'name', 'desc', 'detail', 'is_banner', 'degree', 'learn_times', 'students', 'favor_nums', 'click_nums', 'add_time']
    search_fields = ['course_org', 'name', 'desc', 'detail', 'degree', 'students', 'favor_nums', 'click_nums']
    list_filter = ['course_org', 'name', 'desc', 'detail', 'is_banner', 'degree', 'learn_times', 'students', 'favor_nums', 'click_nums', 'add_time']
    model_icon = 'fa fa-book'
    readonly_fields = ['click_nums', 'favor_nums', 'students']
    relfield_style = 'fk-ajax'
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # 由于lesson中的course字段涉及到外键Course,所以在filter中要写入course__name
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fa fa-calendar-check-o'
    relfield_style = 'fk-ajax'

class VedioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']
    model_icon = 'fa fa-video-camera'

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']
    model_icon = 'fa fa-share-alt'

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VedioAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
