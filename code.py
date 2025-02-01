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


# ✅ 사용자가 직접 이미지 폴더 입력 가능 (기본값: "images/")
default_folder = "images"
image_folder = input(f" 분석할 이미지 폴더를 입력하세요 (기본값: {default_folder}): ").strip()
if image_folder == "":
    image_folder = default_folder  # 기본값 설정

# ✅ 결과 저장 폴더 설정
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ✅ 선택한 폴더에서 모든 이미지 가져오기
image_files = glob.glob(os.path.join(image_folder, "*.jpg")) + glob.glob(os.path.join(image_folder, "*.png"))

if len(image_files) == 0:
    print(f"⚠ {image_folder} 폴더에 이미지가 없습니다. 확인 후 다시 실행하세요.")
    exit()

# 사진 및 표기되는 텍스트, 라인 출력 관련 옵션
pcv.params.dpi = 100
pcv.params.text_size = 20
pcv.params.text_thickness = 20
pcv.params.line_thickness = 10


# ✅ 이미지 분석 실행
for image_path in image_files:
    img, path, filename = pcv.readimage(image_path)

    crop_img = pcv.crop(img=img, x=0, y=0, h=2500, w=3000)

    # CMYK Y채널 변환
    h_channel = pcv.rgb2gray_cmyk(rgb_img=crop_img, channel='y')

    bin_img = pcv.threshold.binary(gray_img=h_channel, threshold=15, object_type="dark")

    fill_mask = pcv.fill(bin_img=bin_img, size=200)

    analysis_image = pcv.analyze.size(img=crop_img, labeled_mask=fill_mask)

    # 결과 저장
    result_path = os.path.join(output_folder, f"processed_{filename}")
    pcv.print_image(analysis_image, result_path)

    print(f" {filename} 분석 완료!")

print(" 모든 이미지 분석 완료!")


    



