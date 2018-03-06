from django.test import TestCase

# Create your tests here.
a={3: {'id': 3, 'caption': '账户操作', 'parent_id': 1, 'opened': False, 'status': False, 'child': []},
 4: {'id': 4, 'caption': '订单管理', 'parent_id': None, 'opened': False, 'status': True,
     'child': [{'id': 5, 'caption': '订单记录', 'parent_id': 4, 'opened': False, 'status': False, 'child': []},
               {'id': 6, 'caption': '评分系统', 'parent_id': 4, 'opened': False, 'status': True,
                'child': [{'id': 7, 'caption': '用户评分', 'parent_id': 6, 'opened': False, 'status': False, 'child': []},
                          {'id': 8, 'caption': '系统评分', 'parent_id': 6, 'opened': False, 'status': True, 'child': [
                              {'id': 8, 'caption': '权限10', 'url': '/info.html', 'parent_id': 8, 'opened': False,
                               'status': True}]}]}]},
 5: {'id': 5, 'caption': '订单记录', 'parent_id': 4, 'opened': False, 'status': False, 'child': []},
 6: {'id': 6, 'caption': '评分系统', 'parent_id': 4, 'opened': False, 'status': True,
     'child': [{'id': 7, 'caption': '用户评分', 'parent_id': 6, 'opened': False, 'status': False, 'child': []},
               {'id': 8, 'caption': '系统评分', 'parent_id': 6, 'opened': False, 'status': True, 'child': [
                   {'id': 8, 'caption': '权限10', 'url': '/info.html', 'parent_id': 8, 'opened': False,
                    'status': True}]}]},
 7: {'id': 7, 'caption': '用户评分', 'parent_id': 6, 'opened': False, 'status': False, 'child': []},
 8: {'id': 8, 'caption': '系统评分', 'parent_id': 6, 'opened': False, 'status': True,
     'child': [{'id': 8, 'caption': '权限10', 'url': '/info.html', 'parent_id': 8, 'opened': False, 'status': True}]}}
