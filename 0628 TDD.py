06-28 목 12일차 - TDD 

새 프로젝트 생성 test2
pip install django
django-admin startproject config .


DRF(Django Rest Framework)는 백엔드만 rest API로 만드는 것

TDD 개발 방법 
Test가 우선이 됨
테스트코드 부터 짜고나서, 테스트코드에 맞게 기능을 개발함 
단위 테스트, 통합 테스트, 기능 테스트 -> 3가지 
단위 테스트: 가장 작은 단위 -> view 등을 하나하나 다 테스트함
통합 테스트 : 데이터베이스나 서버 등을 통합해서 테스트함 

ex) 제목을 너무 짧게 지으면 안 되게 한다거나, 로그인 페이지가 잘 뜬다든가, 위지위그 검증해서 사용자가 잘 못 입력했다면 메세지를 띄움 

python manage.py startapp board 

board/test.py 지우고, 
board/tests/  패키지 디렉토리 생성해서 여기에 테스트 스크립트 작성
test_urls.py, test_form.py, test_view.py 등 

테스트 없이 코드를 작성한다면
views, models, urls, settings, forms, html

장고 사이클
사용자 -> url -> 장고에 요청
urls.py에 매핑된 함수가 실행
html 반환 


test_urls.py 파일 생성 
from django.test import TestCase
from django.urls import resolve 
from board.views import create

class TestUrls(TestCase): # TestCase를 상속받는 TestUrls 클래스 생성
	def test_create_url_is_resolved(self): 
		url = resolve(‘/board/create’) # 해당 url을 찾음 
		self.assertEqual(url.func, create) # 같은지 비교 

views.py
def create(request):
	pass 

urls.py
path(‘board/create’, board.views.create)

python .\manage.py test 실행하면 알아서 여러 앱들에서 테스트 코드를 다 찾음

test_view.py 파일 생성
from django.test import TestCase, Client 

class TestViews(TestCase):
	def setup(self):
		self.client = Client()
	
	def test_post_create_GET(self):
		
from django.test import TestCase, Client

class TestViews(TestCase):
    def setup(self):
        self.client = Client()

    def test_post_create_GET(self):
        response = self.client.get('/board/create') # board/create에 get 방식으로 요청을 했을 때,

        self.assertEqual(response.status_code, 200) # 정상적으로 받아갔다면 200코드
        self.assertTemplateUsed(response, 'board/create.html') # 어떤 템플릿 썼는지 확인
		
템플릿 폴더 만들어서
templates/board/create.html 파일 만들기 

settings.py에서 
TEMPLATES = [
    {      
        'DIRS': [BASE_DIR / 'templates'],

views.py 
def create(request):
	return render(request, 'board/create.html')
	
python manage.py test 실행 
점 2개 찍힘 (테스트케이스 하나 당 점 하나)

특정 테스트케이스만 실행하고 싶을 떄 
python manage.py test board.tests.test_views


python manage.py test board.tests.test_views.Test.Views.test_post_create_GET

==========================================================================================

from django.test import TestCase, Client

class TestViews(TestCase):
    def setup(self):
        self.client = Client()

    def test_post_create_GET_with_login(self):
        response = self.client.get('/board/create') # board/create에 get 방식으로 요청을 했을 때,

        self.assertEqual(response.status_code, 200) # 정상적으로 받아갔다면 200코드
        self.assertTemplateUsed(response, 'board/create.html') # 어떤 템플릿 썼는지 확인
		
템플릭 폴더 만들어서
templates/board/create.html 파일 만들기 

settings.py에서 
TEMPLATES = [
    {      
        'DIRS': [BASE_DIR / 'templates'],

views.py 
def create(request):
	return render(request, 'board/create.html')
	
python manage.py test 실행 
점 2개 찍힘 (테스트케이스 하나 당 점 하나)

특정 테스트케이스만 실행하고 싶을 떄 
python manage.py test board.tests.test_views


python manage.py test board.tests.test_views.Test.Views.test_post_create_GET

==================================================================================================

login 여부에 따른 테스트케이스 
class TestViews(TestCase):
    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user01', password='qwer1234!')# 로그인 여부에 따라 테스트하기 위해 사용자를 하나 추가함

    def test_post_create_GET_with_login(self): # 로그인을 했다면 html을 반환해야함
        self.client.login(username='user01', password='qwer1234!') # 로그인 코드를 넣음
        response = self.client.get('/board/create') # board/create에 get 방식으로 요청을 했을 때,

        self.assertEqual(response.status_code, 200) # 정상적으로 받아갔다면 200코드
        self.assertTemplateUsed(response, 'board/create.html') # 어떤 템플릿 썼는지 확인


    def test_post_create_GET_without_login(self): # 로그인 페이지가 뜨는지 봐야함
        # 위의 케이스와는 다르게, 로그인 코드를 넣지 않음
        response = self.client.get('/board/create') # board/create에 get 방식으로 요청을 했을 때,

        self.assertEqual(response.status_code, 302) # 정상적으로 리다이렉트하기 위해 302코드
        self.assertTemplateUsed(response, 'accounts/login.html') # 어떤 템플릿 썼는지 확인

@login_required 데코레이터 넣기 
board/views.py
@login_required(login_url='/accounts/login')
def create(request):
    return render(request, 'board/create.html')


모델을 만들어야 함

board/models.py 
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    writer = models.ForiegnKey(User, on_delete=models.CASCADE)
    
    
    
게시글 CRUD 테스트케이스     
from django.test import TestCase
from django.contrib.auth.models import Post
from django.contrib.auth.models import User

class TestModels(TestCase):
    def setup(self):
        self.user = User.objects.create_user(
            username='user01',
            password='qwer1234!'
        )# 로그인 여부에 따라 테스트하기 위해 사용자를 하나 추가함

        self.post = Post.objects.create(
            title='title1',
            contents='contents1',
            writer=self.user
        )

    def test_post_model_create(self):
        post = Post()
        post.title = 'title2'
        post.contents = 'contents'
        post.writer = self.writer
        post.save()

        post = Post.objects.get(title='title2')
        self.assertEqual(post.title, 'title2')

    def test_post_model_read(self):
        post = Post.objects.get(id=1) # 조회하기
        self.assertEqual(post.title, 'title1') # 조회한 값이 저장한 값이랑 같은지 확인 

    def test_post_model_update(self):
        post = Post.objects.get(id=1) # 조회하기
        post.ttle = 'title3' # 타이틀 변경하기
        post.save() # 저장하기

        post = Post.objects.get(id=1) # 다시 조회하기
        self.assertEqual(post.title, 'title3') # 변경이 적용되었는지 확인

    def test_post_model_delete(self):
        post = Post.objects.get(id=1)
        post.delete()

        self.assertFalse(Post.objects.filter(id=1).exists())




python manage.py makemigrations
python manage.py migrate 

POST 방식 확인 
test_view.py 
    def test_post_create_POST_with_login(self):  # 로그인을 했다면 html을 반환해야함
        self.client.login(username='user01', password='qwer1234!')  # 로그인 코드를 넣음
        response = self.client.post(
            '/board/create',
            data={'title':'title1', 'contents': 'contents1'}
        )  
        
        post = Post.objects.get(title='title1') # 게시글이 저장됐는지 확인 
        self.assertEqual(post.title, 'title1')
        self.assertEqual(response.status_code, 302)  # 정상적으로 리다이렉트 됐다면 302 코드

위에 맞게 views.py에서 함수 작성 
@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'GET':
        return render(request, 'board/create.html')

    elif request.method == 'POST':
        post = Post()
        post.title = request.Post.get('title')
        post.contents = request.Post.get('contents')
        post.writer = request.user
        post.save()
        return redirect('/board/read' + str(post.id))
        

게시글 제목이 5글자 미만이면 에러페이지로 리다이렉트하는 테스트케이스 작성하기 
test_view.py
    def test_post_create_POST_with_check_title_length(self):
        self.client.login(username='user01', password='qwer1234!')  # 로그인 코드를 넣음
        response = self.client.post(
            '/board/create',
            data={'title': 'a', 'contents': 'contents1'} # 타이틀에 한 글자만 입력하면 
        )
        self.assertEqual(response.url, '/error')
        self.assertEqual(response.status_code, 302)  # 정상적으로 리다이렉트 됐다면 302 코드

views.py
@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'GET':
        return render(request, 'board/create.html')

    elif request.method == 'POST':
        post = Post()
        post.title = request.POST.get('title')
        if len(post.title) < 5: # 5 글자보다 작으면 
            return redirect('/error') # 에러 페이지 리다이렉트 

        post.contents = request.POST.get('contents')
        post.writer = request.user
        post.save()
        return redirect('/board/read' + str(post.id))


게시글 작성 form 만들기 
board/forms.py
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'contents', )
        exclude = ('writer', )

board.views.py 
@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'GET':
        postForm = PostForm()

        return render(request, 'board/create.html', {'postForm': postForm})
        
        
보드 테스트하기 
python manage.py createsuperuser 슈퍼유저 생성 
python manage.py runserver 
127.0.0.1:8000/admin에서 admin으로 로그인 후 board/create 페이지로 들어오기 

        
에러 메세지 출력 
views.py 
from django.contrib import messages

    if len(post.title) < 5:
        messages.add_message(request, messages.ERROR, '제목은 5글자 이상이여야 합니다')
        context['has_error'] = True
            
            
create.html의 폼태그 바깥에 추가 
{% if messages %}
    {% for message in messages %}
        {% if message.tags == 'error' %}
            {{ message }}
        {% endif %}
    {% endfor %}
{% endif %}

에러메세지 테스트케이스 
test_view.py에 
def test_post_create_POST_with_check_title_length(self):
    self.client.login(username='user01', password='qwer1234!')  # 로그인 코드를 넣음
    response = self.client.post(
        '/board/create',
        data={'title': 'a', 'contents': 'contents1'}
    )
    messages = list(response.context['messages'])
    self.assertEqual(len(messages), 1) # 에러가 하나 발생
    self.assertEqual(str(messages[0]), '제목은 5글자 이상이어야 합니다.')
    self.assertEqual(response.status_code, 400)  # 정상적으로 리다이렉트 됐다면 302 코드

views.py 
if context['has_error']: # 에러 있으면 리턴
    return render(request, 'board/create.html', context, status=400) # 클라이언트 잘못이니까 에러 400 
post.save() # 에러 없으면 저장        
       
전체 코드 
views.py 
@login_required(login_url='/accounts/login')
def create(request):
    if request.method == 'GET':
        postForm = PostForm()

        return render(request, 'board/create.html', {'postForm': postForm})

    elif request.method == 'POST':
        postForm = PostForm(request.POST)
        context = {
            'postForm': postForm,
            'has_error': False # 에러 있나 없나 변수 생성하기
        }

        post = Post()
        post.title = request.POST.get('title')
        if len(post.title) < 5:
            messages.add_message(request, messages.ERROR, '제목은 5글자 이상이여야 합니다')
            context['has_error'] = True

        post.contents = request.POST.get('contents')
        post.writer = request.user

        if context['has_error']: # 에러 있으면 리턴
            return render(request, 'board/create.html', context)
        post.save() # 에러 없으면 저장

        return redirect('/board/read' + str(post.id))


=================================================================================================

로그인한 사람한테만 수정, 삭제 버튼 보이게 
-> 게시글 조회 기능 만들기

def setup에 user02 추가, user01이 작성한 post도 추가 

    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user01', password='qwer1234!')# 로그인 여부에 따라 테스트하기 위해 사용자를 하나 추가함
        self.user = User.objects.create_user(username='user02', password='qwer1234!')# 로그인 여부에 따라 테스트하기 위해 사용자를 하나 추가함
        self.post = Post.objects.create(
            title='title1',
            contents='contents1',
            writer=self.user
        )

test_view.py        
def test_post_read_GET_with_writer(self):
    pass

def test_post_read_GET_without_writer(self):
    pass

def test_post_Read_GET_with_other_writer(self):
    pass

테스트 케이스
view가 템플릿 반환 -> 게시글 조회 템플릿에서 게시글 작성 사용자와 로그인한 사용자가 같으면 수정/삭제 가능

urls.py    
path('board/read/<int:bid>', board.views.read)

views.py
def read(request, bid):
    post = Post.objects.get(id=bid)

    context = {'post': post}
    return render(request, 'board/read.html', context)

read.html
{% if post %}
    {{post.title}}
    {{post.contents}}
        {% if request.user == post.writer %}
            <button>수정</button>
            <button>삭제</button>
        {% endif %}
{% endif %}

test_views.py
def test_post_read_GET_with_writer(self): #
    response = self.client('/board/read/1') # 실제 db에는 없어도, 위에 테스트케이스로 인해 1번 post가 있음
    self.assertTemplateUsed(response, 'board/read.html')
    self.assertInHTML('<button>수정</button>', response.render_content)

