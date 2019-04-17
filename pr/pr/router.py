from api.viewsets import *
from rest_framework import routers
from api.viewsets import *

router = routers.DefaultRouter()
router.register(r'user', UserViewset, base_name = 'allusers')
router.register(r'posting', PostingViewset, base_name = 'postings')
router.register(r'sdashboard',StuDashboardViewset, base_name = 'studash')
