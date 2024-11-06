from rest_framework import status

from api.wallet.serializers.identification import IdentificationSerializer, \
    IdentificationSerializers, NotificationSerializer
from apps.accounts.models import NotificationModel
from apps.wallet.models import Identification
from rest_framework.response import Response
from datetime import datetime, timedelta, time


from services.unigate.identification.method import get_access_token, get_user_profile


#update

def identification(request):
    data = request.data
    serializer = IdentificationSerializer(data=data)
    if serializer.is_valid():
        # current_datetime = datetime.now()
        # start_time = time(17, 0, 0)  # 17:00:00
        # end_time = time(4, 0, 0)  # 04:00:00
        #
        # # Adjust end_time to the next day if necessary
        # if start_time < end_time:
        #     # Normal case: e.g., 17:00 - 04:00
        #     if start_time <= current_datetime.time() < end_time:
        #         return Response({"message": 'Error'}, status=status.HTTP_403_FORBIDDEN)
        # else:
        #     # Overnight case: e.g., 17:00 - 23:59 and 00:00 - 04:00
        #     if current_datetime.time() >= start_time or current_datetime.time() < end_time:
        #         return Response({"message": 'Error'}, status=status.HTTP_403_FORBIDDEN)

        response = get_access_token(code=data['code'])


        if 'access_token' in response:
            identification = Identification()
            identification.user = request.user
            identification.code = data['code']
            identification.access_token = response['access_token']
            identification.image = data['image']
            identification.expires_in = response['expires_in']
            identification.token_type = response['token_type']
            identification.scope = response['scope']
            identification.refresh_token = response['refresh_token']
            identification.comparison_value = response['comparison_value']
            identification.save()

            response = get_user_profile(access_token=identification.access_token)
            if 'profile' in response:
                identification.seria = response['profile']['doc_data']['pass_data']
                identification.pinfl = response['profile']['common_data']['pinfl']
                identification.response = response
                identification.save()
                return Response({'message': 'Success'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def my_id_user_info(request):
    identification = Identification.objects.filter(user=request.user).first()
    if not identification:
        return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializers = IdentificationSerializers(identification)
    response = serializers.data.get('response')
    profile = response.get('profile')
    return Response(profile)


def notification(request):
    notification = NotificationModel.objects.all()
    serializer = NotificationSerializer(notification, many=True)

    return Response(serializer.data)