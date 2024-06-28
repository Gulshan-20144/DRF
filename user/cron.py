from rest_framework.response import Response
from rest_framework import status
import logging 
from user.views import ChangePasswordView
logger=logging.getLogger(__name__)

def prints(request):
    print("ddddddddddddddd")
    ChangePasswordView.post()
    logger.info("this is cron job")