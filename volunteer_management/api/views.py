from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Volunteer, Organizer, Activity, ActivityStatus, ActivityApplication, VolunteerActivity
from .serializers import VolunteerSerializer, OrganizerSerializer, ActivitySerializer, ActivityStatusSerializer, ActivityApplicationSerializer, VolunteerActivitySerializer
from rest_framework.permissions import IsAuthenticated
import jwt
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, F, Q
from django.contrib.auth import update_session_auth_hash
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

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
                    tagged_activities = activities.filter(activity_tags=tag).values()[:1]  # 每个标签取最多3个活动
                    activity_data.extend(tagged_activities)  # 将找到的活动添加到结果列表中

                    # 如果已经找到了3个活动，退出循环
                    if len(activity_data) >= 3:
                        break

            # 如果没有找到用户喜欢的活动，则返回所有招募中的活动
            if not activity_data:
                activity_data = list(activities.values())[:3]  # 限制返回3个活动

            return Response(list(activity_data)[:3])  # 确保返回的列表最多为3个活动

        elif tab == 'hot':
            hot_activities = Activity.objects.filter(
                activitystatus__activity_status='进行中'
            ).annotate(total_clicks=F('activitystatus__total_clicks')).order_by('-total_clicks')[:3]
            # 只选择需要的字段，并将结果转换为列表
            activity_data = list(hot_activities.values())[:3]  # 确保最多返回3个活动
            return Response(activity_data)  # 直接返回活动列表

        return Response({'error': '无效的标签'}, status=400)


class UserActivityPagination(PageNumberPagination):
    page_size = 4  # 每页活动数量
    page_size_query_param = 'page_size'
    max_page_size = 10

class UserActivityView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取用户参与的活动
        volunteer_activities = VolunteerActivity.objects.filter(student_id=user_id)

        # 处理状态过滤
        status_filter = request.GET.get('status')
        if status_filter:
            volunteer_activities = volunteer_activities.filter(activity_result=status_filter)

        # 处理搜索查询
        search_query = request.GET.get('search')
        if search_query:
            volunteer_activities = volunteer_activities.filter(
                Q(activity__activity_name__icontains=search_query) |
                Q(activity__activity_location__icontains=search_query) |
                Q(activity__organizer__name__icontains=search_query)  # 假设你有一个组织者的名字字段
            )

        paginator = UserActivityPagination()
        paginated_activities = paginator.paginate_queryset(volunteer_activities, request)

        # 序列化活动数据
        serializer = ActivitySerializer([va.activity for va in paginated_activities], many=True)
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
        file = request.data.get('file')

        if file:
            # 修改存储路径为frontend/public下
            storage_location = r'D:\jiaotongdaxue\web_developmet\volunteer_management\frontend\public\activity-images'
            fs = FileSystemStorage(location=storage_location)
            filename = fs.save(file.name, file)
            file_url = f"/activity-images/{filename}"  # 访问时使用相对路径

            return Response({'url': file_url}, status=201)
        else:
            return Response({'error': 'No file uploaded'}, status=400)


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
    def post(self, request, activity_id_hash):
        try:
            activity = Activity.objects.get(activity_id=activity_id_hash)
            # 假设这里进行报名逻辑，比如检查名额、更新数据库等
            activity_status = ActivityStatus.objects.get(activity=activity)

            if activity_status.registered_volunteers < activity_status.accepted_volunteers:
                activity_status.registered_volunteers += 1
                activity_status.save()
                return Response({'message': '报名成功！'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '名额已满！'}, status=status.HTTP_400_BAD_REQUEST)
        except Activity.DoesNotExist:
            return Response({'error': '活动不存在'}, status=status.HTTP_404_NOT_FOUND)
        except ActivityStatus.DoesNotExist:
            return Response({'error': '活动状态不存在'}, status=status.HTTP_404_NOT_FOUND)