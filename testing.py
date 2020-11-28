# coding: utf-8
#
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import SessionAuthentication
# from rest_framework.authentication import BasicAuthentication
#
# from rest_framework.authentication import TokenAuthentication
#
# from django.contrib.auth.middleware import AuthenticationMiddleware
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.middleware.csrf import CsrfViewMiddleware
#
# from django_user_agents.middleware import UserAgentMiddleware


# import json
# import pickle
#
# data = {
#     'key1': 'value1',
#     'key2': 'value2'
# }
#
# ret = json.dumps(data)
#
# print(ret.encode('utf-8'))
# print(type(ret.encode('utf-8')))
#
# ret1 = pickle.dumps(data)
# print(ret1)
# print(type(ret1))


from collections import Counter

l1 = [1, 2, 3, 1, 1, 2]
ret1 = Counter(l1)
print(ret1)


l2 = [[1, 2], 2, 2, 3]
ret2 = Counter(l2)
print(ret2)




