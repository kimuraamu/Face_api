import streamlit as st
import io
import requests
from PIL import Image, ImageDraw, ImageFont


st.title("顔認識AIアプリ")

#サブスクリプションキーの入力
KEY = "67304730480c4a0d854ded995920a750"
assert KEY

face_api_url = "https://20201211faceapi.cognitiveservices.azure.com/face/v1.0/detect"

st.write("画像選択")

upload_file = st.file_uploader("choose image",type = "jpg")

#画像がアップロードされていれば実行する
if upload_file is not None:
    img = Image.open(upload_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")

        #バイナリデータを取得する
        binary_img = output.getvalue()

#------Apiのメイン機能--------
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': KEY}

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': "age,gender,headPose,smile,facialHair,glasses,emotion," +
                                "hair,makeup,occlusion,accessories,blur,exposure,noise"
    }
#postでAPIリクエストを送信
    response = requests.post(face_api_url, params=params,
                             headers=headers, data=binary_img)
# ------Apiのメイン機能--------

#返ってきたAPIをjson形式で表示
    results = response.json()
    for result in results:
        rect = result['faceRectangle']

        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left'] + rect['width'], rect['top'] + rect['height'])],
                       fill=None, outline="red", width=2)

        age = result['faceAttributes']['age']
        gender = result['faceAttributes']['gender']

        str_age = str(age)
        str_gender = str(gender)

        font_size = 20

        draw_x = rect['left'] - 15
        draw_y = rect['top'] - 45
        text = "age : " + str_age + "\n" + "gender : " + str_gender

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/Library/Fonts/Arial Narrow Bold.ttf', font_size)
        draw.text((draw_x, draw_y), text, font=font, fill=(255, 0, 0, 128))

    st.image(img,caption="image",use_column_width=True)
