import os

# 'data/fdr' 폴더의 경로 설정
folder_path = os.path.join("data", "fdr")

# 폴더 내의 모든 파일에 대해 반복
for filename in os.listdir(folder_path):
    # 원래 파일의 전체 경로
    old_file = os.path.join(folder_path, filename)

    # 새 파일명 생성 ('A'를 이름 앞에 추가)
    new_filename = "A" + filename
    new_file = os.path.join(folder_path, new_filename)

    # 파일 이름 변경
    os.rename(old_file, new_file)

    print(f"Renamed '{filename}' to '{new_filename}'")