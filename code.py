#import os
#from zipfile import ZipFile
#from google.colab import files

#environment = detect_notebook_environment()

#!gdown --id 1Gqbq_xEOtmSBp9NUdwa6-UUiQKFMBsSD --output test_1.png

# 라이브러리 import
import ipywidgets, altair
from plantcv import plantcv as pcv
from plantcv.parallel import WorkflowInputs
import glob
os.getcwd()

image_folder = "/content"
uploaded = files.upload()

# ✅ 결과 저장 폴더 설정
output_folder = "/content/output"
output_folder_mask = "/content/output/mask"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if not os.path.exists(output_folder_mask):
    os.makedirs(output_folder_mask)


# ✅ 선택한 폴더에서 모든 이미지 가져오기
image_files = [os.path.join(image_folder, f) for f in uploaded.keys() if f.endswith((".jpg", ".png"))]

import cv2
import csv
pcv.params.debug = None 

# ✅ CSV 파일 설정 (이심률 저장)
csv_filename = os.path.join(output_folder, "eccentricity_results.csv")
for image_path in image_files:
    # 이미지 로드
    
   #img, _, _ = pcv.readimage(filename=image_path)


    # ✅ OpenCV를 사용하여 이미지 로드 (EXIF 자동 회전 방지)

    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED ^ cv2.IMREAD_IGNORE_ORIENTATION)


    # 파일명 가져오기
    filename = os.path.basename(image_path)

    # 이미지 크롭 
    crop_img = pcv.crop(img=img, x=0, y=0, h=2500, w=3000)

    # CMYK Y채널 변환
    h_channel = pcv.rgb2gray_cmyk(rgb_img=crop_img, channel='y')

    # 바이너리 임계값 처리
    bin_img = pcv.threshold.binary(gray_img=h_channel, threshold=15, object_type="dark")

    # 작은 구멍 채우기
    fill_mask = pcv.fill(bin_img=bin_img, size=200)

    # 이미지 분석
    analysis_image = pcv.analyze.size(img=crop_img, labeled_mask=fill_mask)

    # ✅ 이심률(Eccentricity) 값 추출
    eccentricity = None
    if "default_1" in pcv.outputs.observations and "ellipse_eccentricity" in pcv.outputs.observations["default_1"]:
        eccentricity = pcv.outputs.observations["default_1"]["ellipse_eccentricity"]["value"]

    
    # ✅ CSV 파일에 결과 저장
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([filename, eccentricity])

    # ✅ 결과 이미지 저장 경로 설정
    analysis_result_path = os.path.join(output_folder, f"processed_{filename}")
    mask_result_path = os.path.join(output_folder_mask, f"mask_{filename}")

    # ✅ 결과 이미지 & 마스크 이미지 저장
    pcv.print_image(analysis_image, analysis_result_path)
    pcv.print_image(fill_mask, mask_result_path)

    print(f"✔ {filename} 분석 완료! → 저장 경로: {analysis_result_path}, {mask_result_path}")
    print(f"✔ {filename} 이심률 저장 완료! → CSV 파일: {csv_filename}")




    



