# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from operation.models import UserFavorite

from courses.models import Course
from .models import Teacher

# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 授课机构排名
        hot_orgs = all_orgs.order_by('-click_nums')[:5]

        # 城市
        all_cities = CityDict.objects.all()

        # 机构搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 学生或者课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 机构数量
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)

        context = {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        }
        return render(request, 'org-list.html', context)


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # Ajax异步,返回json字符串,content_type声明字符串类型为application/json
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')

class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 取出机构下面的所有课程（用到了course_set）,orm的用法
        all_courses = course_org.course_set.all()[:3]
        # 取出机构下面的所有教师（用到了teacher_set）,orm的用法
        all_teachers = course_org.teacher_set.all()[:1]

        context = {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-homepage.html', context)


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 取出机构下面的所有课程（用到了course_set）,ForeignKey关系数据库反向查询操作
        all_courses = course_org.course_set.all()

        context = {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        context = {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    """
    机构讲师
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 取出机构下面的所有教师（用到了teacher_set）,orm的用法
        all_teachers = course_org.teacher_set.all()

        context = {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-teachers.html', context)


class AddFavView(View):
    """
    用户收藏，用户取消收藏。使用ajax异步
    """
    def post(self, request):
        favor_id = request.POST.get('fav_id', 0)
        favor_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(favor_id), fav_type=int(favor_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()
            # 删除后数量自减
            if int(favor_type) == 1:
                course = Course.objects.get(id=int(favor_id))
                course.favor_nums -= 1
                if course.favor_nums <= 0:
                    course.favor_nums = 0
                course.save()
            elif int(favor_type) == 2:
                course_org = CourseOrg.objects.get(id=int(favor_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums <= 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(favor_type) == 3:
                teacher = Teacher.objects.get(id=int(favor_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums <= 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(favor_id) > 0 and int(favor_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(favor_id)
                user_fav.fav_type = int(favor_type)
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teachers =Teacher.objects.all()
        teacher_nums = all_teachers.count()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))

        # 教师排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        # 排行榜讲师
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        # 对讲师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        context = {
            'all_teachers': teachers,
            'teacher_nums': teacher_nums,
            'sorted_teachers': sorted_teachers,
            'sort': sort
        }
        return render(request, 'teachers-list.html', context)


class TeacherDeatailView(View):
    """
    讲师详情页
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        # 判断是否收藏
        has_teacher_faved = False
        has_org_faved = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_faved = True

            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_faved = True

        # 排行榜讲师
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:5]

        context = {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teachers': sorted_teachers,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved
        }
        return render(request, 'teacher-detail.html', context)