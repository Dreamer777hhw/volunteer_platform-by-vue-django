from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Volunteer, Organizer, Activity, ActivityStatus, ActivityApplication, VolunteerActivity, OrganizerActivity
from .serializers import VolunteerSerializer, OrganizerSerializer, ActivitySerializer, ActivityStatusSerializer, ActivityApplicationSerializer, VolunteerActivitySerializer
# from rest_framework.permissions import IsAuthenticated
import jwt
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, F, Q
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from datetime import datetime
import time
import os
# from django.conf import settings

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer


class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityStatusViewSet(viewsets.ModelViewSet):
    queryset = ActivityStatus.objects.all()
    serializer_class = ActivityStatusSerializer

class ActivityApplicationViewSet(viewsets.ModelViewSet):
    queryset = ActivityApplication.objects.all()
    serializer_class = ActivityApplicationSerializer

class VolunteerActivityViewSet(viewsets.ModelViewSet):
    queryset = VolunteerActivity.objects.all()
    serializer_class = VolunteerActivitySerializer


class LoginView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        user_type = request.data.get('user_type')  # 'volunteer' or 'organizer'

        if user_type == 'volunteer':
            try:
                volunteer = Volunteer.objects.get(student_id=user_id)
                if check_password(password, volunteer.password):
                    token = jwt.encode({'user_id': volunteer.student_id}, 'your_secret_key', algorithm='HS256')

                    # 更新 token 字段和 token_expiration
                    volunteer.token = token
                    volunteer.token_expiration = timezone.now() + timedelta(hours=1)  # 设置过期时间，例如1小时
                    volunteer.save()

                    return Response({'token': token, 'name': volunteer.name}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
            except Volunteer.DoesNotExist:
                return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        elif user_type == 'organizer':
            try:
                organizer = Organizer.objects.get(organizer_id=user_id)  # 根据实际字段名修改
                if check_password(password, organizer.password):
                    token = jwt.encode({'user_id': organizer.organizer_id}, 'your_secret_key', algorithm='HS256')

                    # 更新 token 字段和 token_expiration
                    organizer.token = token
                    organizer.token_expiration = timezone.now() + timedelta(hours=1)  # 设置过期时间，例如1小时
                    organizer.save()

                    return Response({'token': token, 'name': organizer.organizer_name}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
            except Organizer.DoesNotExist:
                return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'error': '无效的用户类型'}, status=status.HTTP_400_BAD_REQUEST)


class AutoTokenLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            # 解码 token
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            user_id = payload.get('user_id')

            # 查找用户
            volunteer = Volunteer.objects.filter(student_id=user_id).first()
            if volunteer:
                return Response({'message': '自动登录成功！', 'user_id': volunteer.student_id}, status=status.HTTP_200_OK)

            organizer = Organizer.objects.filter(organizer_id=user_id).first()
            if organizer:
                return Response({'message': '自动登录成功！', 'user_id': organizer.organizer_id}, status=status.HTTP_200_OK)

            return Response({'error': '无效的 token'}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'token 已过期'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': '无效的 token'}, status=status.HTTP_401_UNAUTHORIZED)

class AutoPasswdLoginView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        user_type = request.data.get('user_type')  # 'volunteer' or 'organizer'

        if user_type == 'volunteer':
            try:
                volunteer = Volunteer.objects.get(student_id=user_id)
                if check_password(password, volunteer.password):
                    return Response({'message': '凭据自动登录成功！', 'user_id': volunteer.student_id}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
            except Volunteer.DoesNotExist:
                return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        elif user_type == 'organizer':
            try:
                organizer = Organizer.objects.get(organizer_id=user_id)  # 根据实际字段名修改
                if check_password(password, organizer.password):
                    return Response({'message': '凭据自动登录成功！', 'user_id': organizer.organizer_id}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
            except Organizer.DoesNotExist:
                return Response({'error': '账号或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'error': '无效的用户类型'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        try:
            student_id = request.data.get('student_id')
            name = request.data.get('name')
            school = request.data.get('school')
            major = request.data.get('major')
            email = request.data.get('email')
            phone = request.data.get('phone')
            password = request.data.get('password')

            # 验证是否已存在
            if Volunteer.objects.filter(student_id=student_id).exists():
                return Response({'message': '学号已注册，请更换学号'}, status=status.HTTP_400_BAD_REQUEST)
            if Volunteer.objects.filter(email=email).exists():
                return Response({'message': '邮箱已注册，请更换邮箱'}, status=status.HTTP_400_BAD_REQUEST)

            # 创建新的 Volunteer
            volunteer = Volunteer.objects.create(
                student_id=student_id,
                name=name,
                school=school,
                major=major,
                email=email,
                phone=phone,
                password=make_password(password),  # 加密密码
                application_date=timezone.now().date(),
                labor_hours=0
            )

            return Response({'message': '注册成功！'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'message': '注册失败', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AccountView(APIView):
    def get(self, request, token):
        try:
            # 解码token
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            student_id = payload['user_id']  # 提取 user_id

            # 查询用户信息
            volunteer = Volunteer.objects.get(student_id=student_id)
            return Response({
                'student_id': volunteer.student_id,
                'name': volunteer.name,
                'school': volunteer.school,
                'major': volunteer.major,
                'email': volunteer.email,
                'phone': volunteer.phone,
            }, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token已过期'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.DecodeError:
            return Response({'error': 'Token解码失败'}, status=status.HTTP_401_UNAUTHORIZED)
        except Volunteer.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

class ActivityDetailView(APIView):
    def get(self, request, activity_id_hash):
        try:
            activity = Activity.objects.get(activity_id=activity_id_hash)
            # 获取对应的活动状态
            activitystatus = ActivityStatus.objects.get(activity_id=activity_id_hash)

            activitystatus.clicks_in_1h += 1
            activitystatus.clicks_in_12h += 1
            activitystatus.total_clicks += 1
            activitystatus.save()

            data = {
                'activity_id': activity.activity_id,
                'activity_name': activity.activity_name,
                'activity_description': activity.activity_description,
                'activity_tags': activity.activity_tags,
                'activity_image_path': activity.activity_image_path,
                'application_requirements': activity.application_requirements,
                'application_start_time': activity.application_start_time,
                'application_end_time': activity.application_end_time,
                'activity_start_time': activity.activity_start_time,
                'activity_end_time': activity.activity_end_time,
                'estimated_volunteer_hours': activity.estimated_volunteer_hours,
                'activity_location': activity.activity_location,
                'contact_name': activity.contact_name,
                'contact_phone': activity.contact_phone,
                'organizer': activity.organizer.organizer_name,
                'accepted_volunteers': activity.accepted_volunteers,
                'registered_volunteers': activitystatus.registered_volunteers,
                'activity_status': activitystatus.activity_status,
                'clicks_in_1h': activitystatus.clicks_in_1h,
                'clicks_in_12h': activitystatus.clicks_in_12h,
                'total_clicks': activitystatus.total_clicks,
                'labor_hours': activity.labor_hours,
                'sutuo': activity.sutuo,
                'notes': activity.notes,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            return Response({'error': '活动不存在'}, status=status.HTTP_404_NOT_FOUND)
        except ActivityStatus.DoesNotExist:
            return Response({'error': '活动状态不存在'}, status=status.HTTP_404_NOT_FOUND)

class ActivityListView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        data = []
        for activity in activities:
            # print(activity.activity_id)
            activitystatus = ActivityStatus.objects.get(activity_id=activity.activity_id)
            data.append({
                'activity_id': activity.activity_id,
                'activity_name': activity.activity_name,
                'activity_description': activity.activity_description,
                'activity_tags': activity.activity_tags,
                'activity_image_path': activity.activity_image_path,
                'application_requirements': activity.application_requirements,
                'application_start_time': activity.application_start_time,
                'application_end_time': activity.application_end_time,
                'activity_start_time': activity.activity_start_time,
                'activity_end_time': activity.activity_end_time,
                'estimated_volunteer_hours': activity.estimated_volunteer_hours,
                'activity_location': activity.activity_location,
                'contact_name': activity.contact_name,
                'contact_phone': activity.contact_phone,
                'organizer': activity.organizer.organizer_name,
                'accepted_volunteers': activity.accepted_volunteers,
                'registered_volunteers': activitystatus.registered_volunteers,
                'activity_status': activitystatus.activity_status,
                'clicks_in_1h': activitystatus.clicks_in_1h,
                'clicks_in_12h': activitystatus.clicks_in_12h,
                'total_clicks': activitystatus.total_clicks,
                'labor_hours': activity.labor_hours,
                'sutuo': activity.sutuo,
                'notes': activity.notes,
            })
        return Response(data, status=status.HTTP_200_OK)


class RecommendActivityView(APIView):
    def get(self, request, tab, username):
        if tab == 'recommend':
            # 获取招募中的活动
            activities = Activity.objects.filter(
                activitystatus__activity_status='招募中',
            )
            activity_data = []
            # 筛选当前用户最喜爱的活动类型
            user_favorite_tags = VolunteerActivity.objects.filter(student_id=username).values(
                'activity__activity_tags').annotate(count=Count('activity')).order_by('-count')

            # 如果用户有最喜欢的标签，按标签筛选活动
            if user_favorite_tags.exists():
                for user_favorite_tag in user_favorite_tags:
                    tag = user_favorite_tag['activity__activity_tags']
                    # 从招募中的活动中筛选出包含该标签的活动
                    tagged_activities = activities.filter(activity_tags=tag)[:3]  # 每个标签最多取3个活动
                    activity_data.extend(tagged_activities)  # 将找到的活动添加到结果列表

                    # 如果已经找到了3个活动，退出循环
                    if len(activity_data) >= 3:
                        break

            # 如果没有找到用户喜欢的活动，则返回所有招募中的活动
            if not activity_data:
                activity_data = list(activities)[:3]  # 限制返回3个活动

            # 使用 ActivitySerializer 进行序列化
            serializer = ActivitySerializer(activity_data, many=True)
            return Response(serializer.data)  # 返回序列化后的活动数据

        elif tab == 'hot':
            hot_activities = Activity.objects.filter(
                activitystatus__activity_status='进行中'
            ).annotate(total_clicks=F('activitystatus__total_clicks')).order_by('-total_clicks')[:3]

            # 使用 ActivitySerializer 进行序列化
            serializer = ActivitySerializer(hot_activities, many=True)
            return Response(serializer.data)  # 返回序列化后的活动数据

        return Response({'error': '无效的标签'}, status=status.HTTP_400_BAD_REQUEST)


class UserActivityPagination(PageNumberPagination):
    page_size = 4  # 每页活动数量
    page_size_query_param = 'page_size'
    max_page_size = 10

class UserActivityView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        user_type = request.GET.get('user_type')  # 假设前端会传递 user_type
        if not user_id or not user_type:
            return Response({'error': 'user_id and user_type are required'}, status=status.HTTP_400_BAD_REQUEST)

        # 根据用户类型获取活动
        if user_type == 'volunteer':
            volunteer_activities = VolunteerActivity.objects.filter(student_id=user_id)

        elif user_type == 'organizer':
            organizer_activities = OrganizerActivity.objects.filter(organizer_id=user_id)

        else:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)

        # 处理状态过滤
        status_filter = request.GET.get('status')
        if status_filter:
            if user_type == 'volunteer':
                volunteer_activities = volunteer_activities.filter(activity_result=status_filter)
            elif user_type == 'organizer':
                organizer_activities = organizer_activities.filter(activity_result=status_filter)

        # 处理搜索查询
        search_query = request.GET.get('search')
        if search_query:
            if user_type == 'volunteer':
                volunteer_activities = volunteer_activities.filter(
                    Q(activity__activity_name__icontains=search_query) |
                    Q(activity__activity_location__icontains=search_query) |
                    Q(activity__organizer__organizer_name__icontains=search_query)  # 注意这里的连接
                )
            elif user_type == 'organizer':
                organizer_activities = organizer_activities.filter(
                    Q(activity__activity_name__icontains=search_query) |
                    Q(activity__activity_location__icontains=search_query)
                )

        # 分页处理
        paginator = UserActivityPagination()
        if user_type == 'volunteer':
            paginated_activities = paginator.paginate_queryset(volunteer_activities, request)
            serializer = ActivitySerializer([va.activity for va in paginated_activities], many=True)
        else:
            paginated_activities = paginator.paginate_queryset(organizer_activities, request)
            serializer = ActivitySerializer([oa.activity for oa in paginated_activities], many=True)

        return paginator.get_paginated_response(serializer.data)


class PasswordChangeView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        print("Received POST request")
        try:
            token = request.data.get('token')
            # 解码token
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            student_id = payload['user_id']  # 提取 user_id

            # 查询用户信息
            volunteer = Volunteer.objects.get(student_id=student_id)
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            # 检查旧密码是否正确
            if not check_password(old_password, volunteer.password):
                return Response({'error': '旧密码错误'}, status=status.HTTP_400_BAD_REQUEST)

            # 更新密码
            volunteer.password = make_password(new_password)
            volunteer.save()
            # 更新 session hash
            update_session_auth_hash(request, volunteer)
            return Response({'message': '密码修改成功'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token已过期'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.DecodeError:
            return Response({'error': 'Token解码失败'}, status=status.HTTP_401_UNAUTHORIZED)
        except Volunteer.DoesNotExist:
            return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)


# class UploadImageView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request, *args, **kwargs):
#         file = request.data.get('file')
#
#         if file:
#             fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'activity-images'))
#             filename = fs.save(file.name, file)
#             file_url = f"{settings.MEDIA_URL}activity-images/{filename}"  # 使用正斜杠
#
#             return Response({'url': file_url}, status=201)
#         else:
#             return Response({'error': 'No file uploaded'}, status=400)

class UploadImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        activity_name = request.data.get('activity_name')
        file = request.data.get('file')

        if activity_name and file:
            # 使用活动名称生成安全的文件名
            # safe_activity_name = slugify(activity_name)  # 将活动名称转换为安全的文件名
            # filename = f"{safe_activity_name}.png"  # 使用活动名称作为文件名
            timestamp = int(time.time())  # 获取当前时间戳
            filename = f"{activity_name}_{timestamp}.png"
            # 修改存储路径为frontend/public下
            # storage_location = r'D:\jiaotongdaxue\web_developmet\volunteer_management\frontend\public\activity-images'
            # fs = FileSystemStorage(location=storage_location)
            # fs.save(filename, file)  # 保存文件
            # 修改存储路径为相对路径
            # storage_location = os.path.join('frontend', 'public', 'activity-images')
            storage_location = r'../frontend/public/activity-images'
            fs = FileSystemStorage(location=storage_location)
            fs.save(filename, file)  # 保存文件

            file_url = f"/activity-images/{filename}"  # 访问时使用相对路径

            return Response({'url': file_url}, status=201)
        else:
            return Response({'error': 'Activity name or file not provided'}, status=400)


class CreateActivityView(APIView):
    def post(self, request):
        serializer = ActivitySerializer(data=request.data)

        # 检查数据是否有效
        if serializer.is_valid():
            activity = serializer.save()  # 保存活动到数据库

            # 创建对应的 ActivityStatus 实例
            activity_status_data = {
                'activity': activity.activity_id,  # 设置活动为刚创建的活动
                'activity_status': '未开始',  # 初始状态
                'accepted_volunteers': activity.accepted_volunteers,  # 根据需求设定
                'registered_volunteers': 0,  # 初始报名人数为 0
                'clicks_in_1h': 0,
                'clicks_in_12h': 0,
                'total_clicks': 0,
            }
            status_serializer = ActivityStatusSerializer(data=activity_status_data)

            if status_serializer.is_valid():
                status_serializer.save()  # 保存活动状态到数据库
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 返回验证错误
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterForActivityView(APIView):
    def post(self, request, activity_id_hash, user_id):
        try:
            # 获取活动对象
            activity = Activity.objects.get(activity_id=activity_id_hash)

            # 获取活动状态对象
            activity_status = ActivityStatus.objects.get(activity=activity)

            # 检查名额是否充足
            if activity_status.registered_volunteers < activity_status.accepted_volunteers:
                # 增加已报名人数
                activity_status.registered_volunteers += 1
                activity_status.save()

                # 获取志愿者对象
                student = Volunteer.objects.get(student_id=user_id)

                # 创建新的报名记录
                application = ActivityApplication(
                    student=student,
                    activity=activity,
                    application_result='待审核',  # 默认状态
                    application_date=timezone.now()  # 当前时间
                )
                application.save()

                # 获取或更新志愿者活动记录
                volunteer_activity, created = VolunteerActivity.objects.get_or_create(
                    student=student,
                    activity=activity,
                    defaults={'activity_result': '已报名'}  # 设置状态为已报名
                )
                if not created:
                    # 如果记录已存在，更新状态为已报名
                    volunteer_activity.activity_result = '已报名'
                    volunteer_activity.save()

                return Response({'message': '报名成功！'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '名额已满！'}, status=status.HTTP_400_BAD_REQUEST)
        except Activity.DoesNotExist:
            return Response({'error': '活动不存在'}, status=status.HTTP_404_NOT_FOUND)
        except ActivityStatus.DoesNotExist:
            return Response({'error': '活动状态不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Volunteer.DoesNotExist:
            return Response({'error': '志愿者不存在'}, status=status.HTTP_404_NOT_FOUND)


class UpdateActivityStatusView(APIView):
    def get(self, request):
        try:
            # 获取所有活动状态并更新
            activity_statuses = ActivityStatus.objects.all()
            for activity_status in activity_statuses:
                activity = activity_status.activity

                # 获取当前时间（时区感知）
                now = timezone.now()

                # 将活动的开始和结束时间转换为中国时区
                application_start_time = activity.application_start_time.astimezone(timezone.get_default_timezone())
                application_end_time = activity.application_end_time.astimezone(timezone.get_default_timezone())
                activity_start_time = activity.activity_start_time.astimezone(timezone.get_default_timezone())
                activity_end_time = activity.activity_end_time.astimezone(timezone.get_default_timezone())

                # 判断活动的状态并更新
                if now < application_start_time:
                    activity_status.activity_status = '未开始'
                elif now < application_end_time and activity_status.registered_volunteers < activity_status.accepted_volunteers:
                    activity_status.activity_status = '招募中'
                elif activity_status.registered_volunteers >= activity_status.accepted_volunteers:
                    activity_status.activity_status = '已招满'
                elif now >= activity_start_time and now < activity_end_time:
                    activity_status.activity_status = '进行中'
                elif now >= activity_end_time:
                    activity_status.activity_status = '已结束'
                else:
                    activity_status.activity_status = '已取消'  # 其他情况，视为已取消

                # 保存活动状态更新
                activity_status.save()

                # 更新志愿者活动状态
                volunteer_activities = VolunteerActivity.objects.filter(activity=activity)
                for volunteer_activity in volunteer_activities:
                    if now >= activity_start_time and now < activity_end_time and volunteer_activity.activity_result == '已录取':
                        volunteer_activity.activity_result = '参与中'
                        volunteer_activity.save()
                    elif now >= activity_end_time and volunteer_activity.activity_result == '参与中':
                        volunteer_activity.activity_result = '已参与'
                        volunteer_activity.save()

            return Response({'message': '活动状态更新成功'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityRegistrationsView(APIView):
    def get(self, request, activity_id_hash, user_id):
        # 获取活动对象
        activity = get_object_or_404(Activity, activity_id=activity_id_hash)

        # 根据 user_id 获取该用户的报名记录
        registrations = VolunteerActivity.objects.filter(activity=activity, student_id=user_id)
        activityapplication = ActivityApplication.objects.filter(activity=activity, student_id=user_id)
        # 提取用户 ID 和状态
        registration_data = [
            {
                "student_id": registration.student_id,
                "activity_result": registration.activity_result,
                "application_result": activityapplication.first().application_result
            }
            for registration in registrations
        ]

        if not registration_data:
            return Response({'message': '未找到该用户的报名记录。'}, status=status.HTTP_404_NOT_FOUND)

        return Response(registration_data, status=status.HTTP_200_OK)

class UpcomingActivitiesView(APIView):
    def get(self, request):
        now = timezone.now()
        # 获取开始时间在未来一周内的活动
        upcoming_activities = Activity.objects.filter(activity_start_time__gte=now).order_by('activity_start_time')[:5]

        # 构建响应数据
        activities_data = [
            {
                'name': activity.activity_name,
                'start_time': activity.activity_start_time,
                'link': f'/activity/detail/{activity.activity_id}'  # 假设使用活动 ID 作为链接
            }
            for activity in upcoming_activities
        ]

        return Response(activities_data, status=status.HTTP_200_OK)

class VolunteerApplicationView(APIView):
    def get(self, request, activity_id):
        try:
            # 获取当前活动
            activity = Activity.objects.get(activity_id=activity_id)

            # 获取与活动相关的申请
            applications = ActivityApplication.objects.filter(activity=activity)

            # 序列化申请数据
            application_serializer = ActivityApplicationSerializer(applications, many=True)

            # 序列化活动数据
            activity_serializer = ActivitySerializer(activity)

            # 获取申请中志愿者的相关信息
            volunteer_ids = [app.student.student_id for app in applications]
            volunteers = Volunteer.objects.filter(student_id__in=volunteer_ids)
            volunteer_serializer = VolunteerSerializer(volunteers, many=True)

            # 返回数据
            return Response({
                'activity_name': activity_serializer.data['activity_name'],
                'applications': application_serializer.data,
                'volunteers': volunteer_serializer.data,
            }, status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            return Response({'error': '活动不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApproveVolunteerApplicationView(APIView):
    def patch(self, request, application_id):
        try:
            # 获取申请记录
            application = ActivityApplication.objects.get(application_id=application_id)
            # 更新申请结果为 "已通过"
            application.application_result = '已通过'
            application.save()

            # 创建或更新 VolunteerActivity 记录
            VolunteerActivity.objects.update_or_create(
                student=application.student,
                activity=application.activity,
                defaults={'activity_result': '已录取'}
            )

            return Response({'message': '申请已同意'}, status=status.HTTP_200_OK)
        except ActivityApplication.DoesNotExist:
            return Response({'error': '申请记录不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RejectVolunteerApplicationView(APIView):
    def patch(self, request, application_id):
        try:
            # 获取申请记录
            application = ActivityApplication.objects.get(application_id=application_id)

            # 更新申请结果为 "未通过"
            application.application_result = '未通过'
            application.save()

            # 创建或更新 VolunteerActivity 记录，标记为未录取
            VolunteerActivity.objects.update_or_create(
                student=application.student,
                activity=application.activity,
                defaults={'activity_result': '未录取'}
            )

            return Response({'message': '申请已拒绝'}, status=status.HTTP_200_OK)
        except ActivityApplication.DoesNotExist:
            return Response({'error': '申请记录不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CancelRegistrationView(APIView):

    def post(self, request, activity_id_hash, user_id):
        try:
            # 获取活动和用户
            activity = Activity.objects.get(activity_id=activity_id_hash)
            volunteer = Volunteer.objects.get(student_id=user_id)  # 使用正确的字段名

            # 查找并删除报名记录
            application = ActivityApplication.objects.get(activity=activity, student=volunteer)
            application.delete()  # 删除报名记录

            volunteer_activity = VolunteerActivity.objects.get(student=volunteer, activity=activity)
            if volunteer_activity:
                # 如果记录已存在，更新状态为已取消
                volunteer_activity.activity_result = '已取消'
                volunteer_activity.save()
            else:
                # 如果记录不存在，创建新的志愿者活动记录
                VolunteerActivity.objects.create(student=volunteer, activity=activity, activity_result='已取消')

            # 更新活动的已注册志愿者人数
            activityStatus = ActivityStatus.objects.get(activity=activity)
            activityStatus.registered_volunteers -= 1
            activityStatus.save()

            return Response({"message": "取消报名成功"}, status=status.HTTP_200_OK)

        except Activity.DoesNotExist:
            return Response({"error": "活动不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Volunteer.DoesNotExist:
            return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        except ActivityApplication.DoesNotExist:
            return Response({"error": "未找到报名记录"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserInfoView(APIView):
    def post(self, request):
        user = Volunteer.objects.get(student_id=request.data.get('student_id'))

        # 更新用户信息
        serializer = VolunteerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '用户信息更新成功'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviseActivityDetailView(APIView):
    def get(self, request, activity_id_hash):
        try:
            activity = Activity.objects.get(activity_id=activity_id_hash)
            serializer = ActivitySerializer(activity)
            return Response(serializer.data)
        except Activity.DoesNotExist:
            return Response({"error": "活动未找到"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, activity_id_hash, *args, **kwargs):
        try:
            activity = Activity.objects.get(activity_id=activity_id_hash)
            serializer = ActivitySerializer(activity, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Activity.DoesNotExist:
            return Response({"error": "活动未找到"}, status=status.HTTP_404_NOT_FOUND)


class CalendarView(APIView):
    def get(self, request):
        # 获取日期范围参数
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # 验证日期范围参数
        if not start_date or not end_date:
            return Response({"error": "请提供 start_date 和 end_date 参数"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # 将日期字符串转换为日期对象
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            if start_date is None or end_date is None:
                raise ValueError("日期格式不正确")
        except ValueError:
            return Response({"error": "日期格式不正确，请使用 YYYY-MM-DD 格式"}, status=status.HTTP_400_BAD_REQUEST)

        # 查询在指定日期范围内的所有活动
        activities = Activity.objects.filter(
            Q(activity_start_time__gte=start_date) & Q(activity_end_time__lte=end_date)
        )

        # 序列化活动数据
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActivityClickView(APIView):
    def post(self, request, activity_id):
        try:
            activity_status = ActivityStatus.objects.get(activity_id=activity_id)
            activity_status.total_clicks += 1  # 增加总点击数
            activity_status.clicks_in_1h += 1  # 增加1小时内点击数
            activity_status.save()
            return Response({'message': '点击数已更新'}, status=status.HTTP_200_OK)
        except ActivityStatus.DoesNotExist:
            return Response({'error': '活动不存在'}, status=status.HTTP_404_NOT_FOUND)