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

                    return Response({'token': token}, status=status.HTTP_200_OK)
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

                    return Response({'token': token}, status=status.HTTP_200_OK)
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
    def get(self, request, activity_id):
        try:
            activity = Activity.objects.get(activity_id=activity_id)
            data = {
                'activity_id': activity.activity_id,
                'activity_name': activity.activity_name,
                'activity_description': activity.activity_description,
                'activity_tags': activity.activity_tags,
                'image_path': activity.activity_image_path,
                'application_requirements': activity.application_requirements,
                'application_start_time': activity.application_start_time,
                'application_end_time': activity.application_end_time,
                'activity_start_time': activity.activity_start_time,
                'activity_end_time': activity.activity_end_time,
                'estimated_volunteer_hours': activity.estimated_volunteer_hours,
                'activity_location': activity.activity_location,
                'contact_name': activity.contact_name,
                'contact_phone': activity.contact_phone,
                'organizer': activity.organizer.name,  # 假设 Organizer 有一个 name 字段
                'accepted_volunteers': activity.accepted_volunteers,
                'labor_hours': activity.labor_hours,
                'sutuo': activity.sutuo,
                'notes': activity.notes,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            return Response({'error': '活动不存在'}, status=status.HTTP_404_NOT_FOUND)

class ActivityListView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        data = []
        for activity in activities:
            data.append({
                'activity_id': activity.activity_id,
                'activity_name': activity.activity_name,
                'activity_description': activity.activity_description,
                'activity_tags': activity.activity_tags,
                'image_path': activity.activity_image_path,
                'application_requirements': activity.application_requirements,
                'application_start_time': activity.application_start_time,
                'application_end_time': activity.application_end_time,
                'activity_start_time': activity.activity_start_time,
                'activity_end_time': activity.activity_end_time,
                'estimated_volunteer_hours': activity.estimated_volunteer_hours,
                'activity_location': activity.activity_location,
                'contact_name': activity.contact_name,
                'contact_phone': activity.contact_phone,
                'organizer': activity.organizer.name,  # 假设 Organizer 有一个 name 字段
                'accepted_volunteers': activity.accepted_volunteers,
                'labor_hours': activity.labor_hours,
                'sutuo': activity.sutuo,
                'notes': activity.notes,
            })
        return Response(data, status=status.HTTP_200_OK)