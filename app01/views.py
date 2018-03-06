from django.shortcuts import render,HttpResponse
from app01 import models
from django.db.models import Count
from django.conf import settings
# Create your views here.
def login(request,*args,**kwargs):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        user_name=request.POST.get('username')
        #目标数据结构
        '''
        {'/url正则':['操作方式','GET','DEL','POST','ADD']}
        '''
        #-----------------------------------用户登录成功，就将权限写入session中，将以下代码封装成函数，以便调取-------------
        #1 获取用户对象
        user_obj=models.User.objects.filter(username=user_name).first()
        #2 获取用户角色列表
        # role_list=models.User2Role.objects.filter(user=user_obj).all()   #使用这个不如直接使用role对象查询
        # print(role_list)
        role_list2=models.Role.objects.filter(roles__user=user_obj).all()
        #3 获取用户权限id 和方法
        permission_dict_list=models.Permission2Action2Role.objects.filter(role__in=role_list2).values('permission__url','action__code').all().distinct()  #由于一个人可能有多个角色，故需要去重
        print(permission_dict_list,'permissions')  #<QuerySet [{'permission__url': '/trouble', 'action__code': 'ADD'}, {'permission__url': '/trouble', 'action__code': 'GET'}]>
       #4将数据格式进行修改
        permission_dict={}
        for item in permission_dict_list:
            permission_dict[item['permission__url']]=[]
        for item in permission_dict_list:
            permission_dict[item['permission__url']].append(item['action__code'])
        print(role_list2)
        print(permission_dict,'permission_dict')
        #将用户权限信息写入到session中，用户登录成功，则去获取用户的权限，然后放入session中，当用户去访问其他url时再进行验证
        request.session['permission_dict']=permission_dict
        #-----------------------------将权限挂靠到菜单上-------------------------
        #获取菜单，将url挂靠到菜单上，并写入到session中
        # permision_action_role_obj_list=models.Permission2Action2Role.objects.filter(role__in=role_list2).values('permission__url','action__code')
        # print('-----------permision_action_role_obj_list',permision_action_role_obj_list)
        # user_permission_dict={}         #--------获取用户的权限信息及权限操作方式DEL等-------
        # for item in permision_action_role_obj_list:
        #     if item['permission__url'] in user_permission_dict:
        #         user_permission_dict[item['permission__url']].append(item['action__code'])
        #     else:
        #         user_permission_dict[item['permission__url']]=[item['action__code'],]
        # print('user_permission_dict------------->>',user_permission_dict)   #{'/trouble': ['ADD', 'GET']}
     #获取权限及菜单列表
        permission_list=models.Permission2Action2Role.objects.filter(role__in=role_list2).values(
            'permission_id','permission__url','permission__caption','permission__menu_id').annotate(c=Count('id'))
        print('permission_list   ------->',permission_list)
        #所有的菜单列表
        all_menu_list=models.Menu.objects.values('id','caption','parent_id')
        print('all_menu_list--1---------->>>>',all_menu_list)
        #初始化权限信息的时候，将permission_list及all_menu_list写入到session
        request.session[settings.RBAC_MENU_PERMISSION_SESSION_KEY]={
            settings.RBAC_MENU_KEY:all_menu_list,
            settings.RBAC_PERMISSION_SESSION_KEY:permission_list
        }
        #------------------------------开始结构化菜单列表----------------------
        #---------初始化数据结构字典
        #格式{1: {'id': 1, 'caption': '菜单1', 'parent_id': None, 'opened': False, 'status': False, 'child': []}}
        all_menu_dict={}
        for row in all_menu_list:        #将all_menu_list 加上字段 opened，status，child
            row['opened']=False   #s是否默认展开
            row['status']=False   #是否显示菜单
            row['child']=[]
            all_menu_dict[row['id']]=row
        print(all_menu_dict,'all_menu_dict--------->>>>>>')
        print('all_meun_list----2',all_menu_list)
        for permission in permission_list:
            if not permission['permission__menu_id']:   #如果权限没有菜单，则继续，比如头像上传，就不会挂靠到菜单上
                continue
            temp_item={
                'id': permission['permission_id'],
                'caption':permission['permission__caption'],
                'parent_id': permission['permission__menu_id'],
                'opened': False,
                'status': True,
                'url':permission['permission__url']
            }
            pid=temp_item['parent_id']
            all_menu_dict[pid]['child'].append(temp_item)    #将权限挂靠到菜单上
            print('temp_item---->>>',temp_item)
            if re.match(temp_item['url'],request.path_info):     #如果当前的URL匹配，则当前的URL默认打开
                temp_item['opened']=True
            # if re.match(temp_item['url'],'/view_info/'):     #如果当前的URL匹配，则当前的URL默认打开
            #     temp_item['opened']=True      #测试一下
            temp=pid
            #将当前权限的父级status设置为true
            while not all_menu_dict[temp]['status']:     #如果父级已经是true则不再循环
                all_menu_dict[temp]['status']=True
                temp=all_menu_dict[temp]['parent_id']   #再找上一级父亲
                if not temp:
                    break
            #将当前权限的父辈的opened改为true
            if temp_item['opened']:
                temp1=pid
                while not all_menu_dict[temp1]['opened']:
                    all_menu_dict[temp1]['opened']=True
                    temp1=all_menu_dict[temp1]['parent_id']
                    if not temp1:
                        break
        print('all_meun_dict----2',all_menu_dict)
       #处理菜单之间的等级关系
        result=[]
        for row in all_menu_list:
            pid=row['parent_id']
            if pid:      #如果有parent_id 那么将其添加到all_menu_dict child字段中
                all_menu_dict[pid]['child'].append(row)
            else:   #否则此行数据是父级数据
                result.append(row)
        print('all_meun_dict----3',all_menu_dict)
        print('result',result)   #[{'id': 1, 'caption': '菜单1', 'parent_id': None, 'opened': False, 'status': True,
        # 'child': [{'id': 4, 'caption': '菜单11', 'parent_id': 1, 'opened': False, 'status': True,
        # 'child': [{'id': 1, 'caption': '查看用户信息', 'parent_id': 4, 'opened': False, 'status': True, 'url': '/view_info/'}]},
        def menu_tree(menu_list):
            tpl1 = """
                  <div class='menu-item'>
                      <div class='menu-header'>{0}</div>
                      <div class='menu-body {2}'>{1}</div>
                  </div>
                  """
            tpl2 = """
                  <a href='{0}' class='{1}'>{2}</a>
                  """
            menu_str=''
            for menu in menu_list:
                if menu.get('url'):
                    menu_str+=tpl2.format(menu['url'],'active' if menu['opened'] else '', menu['caption'])
                else:
                    if menu['child']:
                        child_html=menu_tree(menu['child'])
                    else:
                        child_html=''
                    menu_str+=tpl1.format(menu['caption'],child_html,'' if menu['opened'] else 'hide')
            return menu_str



            # if temp_item['opened']:       #如果菜单是展开的
            #     pid=pid
        menu_html=menu_tree(result)
        print('menu_html',menu_html)
        return render(request,'login.html',{'menu_html':menu_html})

import re
def test(request,*args,**kwargs):
    '测试函数，用户访问本URL，则进行验证该用户的session中有没权限（URL，方法）'
    #用户进入访问的格式为  http://127.0.0.1:8000/test/?md=GET
    #------------------------------------封装成中间件，每次访问时必须经过此处进行验证--------------------
    url_visiting=request.path_info  #当前用户访问的url
    print(request.path_info,'当前用户访问的url')
    print(request.GET.get('md'))
    #权限验证
    valid=['/login','/index']         #设置一个列表，内容为不需要进行权限验证的url
    if url_visiting not in valid:
        md = request.GET.get('md')  # 获取当前用户访问url时get传参数的方法，GET，DEL，POST，ADD，EDIT等自己定义的访问方法
        permission_dict = request.session.get('permission_dict')
        if not permission_dict:
            return HttpResponse('无权限访问-------------')
        flag=False
        for key,value in permission_dict.items():
            if re.match(key,url_visiting):
                if md in value:
                    flag=True
                    break
        if not flag:
            return HttpResponse('无权限访问-------------')
    return HttpResponse('it is ok ok ok ok ok ')