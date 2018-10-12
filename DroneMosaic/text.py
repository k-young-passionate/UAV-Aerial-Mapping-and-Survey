gimport zAI
from zAI import zImage
 
 
"""
  "zAI_BACKEND": "local",
  "MICROSOFT_AZURE_TEXT_TRANSLATION_API_KEY": "",
  "MICROSOFT_AZURE_BING_VOICE_API_KEY": "",
  "MICROSOFT_AZURE_FACE_API_KEY": "",
  "GOOGLE_CLOUD_API_KEY": "",
  "MICROSOFT_AZURE_VISION_API_KEY": "",
  "MICROSOFT_AZURE_URL": ""
"""
 
# zAI.utils.set_backend_key(key_name='GOOGLE_CLOUD_API_KEY',key_value='(자신의 API키를 넣는다)',save=True)
zAI.utils.set_backend_key(key_name='MICROSOFT_AZURE_VISION_API_KEY',key_value='6c566e78822847e6995944b7caaf2d51',save=True)
zAI.utils.set_backend_key(key_name='MICROSOFT_AZURE_URL',key_value='eastus.api.cognitive.microsoft.com',save=True)
 
 
# 이미지 지정
image = zImage('/Users/choeyujin/Project/Purdue_Proejct/UAV-Aerial-Mapping-and-Survey/DroneMosaic/2.jpeg')
 
# 이미지 인식
text=image.ocr(backend='Microsoft')
text.display()
 