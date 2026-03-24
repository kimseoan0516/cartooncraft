# cartooncraft

`cartooncraft`는 OpenCV 기반 이미지 처리(양방향 필터 + 에지 추출)를 이용해 입력 이미지를 만화 스타일로 변환하는 프로그램입니다.

## 1) 프로그램 기능

- 입력 이미지 1장을 만화 스타일로 변환
- 간단한 명령어로 결과 이미지 자동 저장
- 비교용 이미지(원본 | 변환본) 생성 지원
- 필터 파라미터 조절로 결과 스타일 튜닝 가능

## 2) 실행 방법

### 실행 환경

- Python 3.9+
- `opencv-python`
- `numpy`

### 설치

```bash
pip install opencv-python numpy
```

### 기본 실행 (가장 간단)

```bash
python cartoon_render.py test.jpg
```

실행 후 같은 폴더에 `test_cartoon.jpg`가 생성됩니다.

### 비교 이미지까지 자동 생성

```bash
python cartoon_render.py test.jpg --comparison auto
```

실행 후 같은 폴더에 아래 파일이 생성됩니다.

- `test_cartoon.jpg`
- `test_compare.jpg` (원본 | 변환 결과)

## 3) 데모: 만화 느낌이 잘 표현된 예시 (2개)

> 아래 2칸에 결과 이미지 파일을 넣어주세요.

### Good Output 1

![Good Output 1](demo/good_output_1.jpg)

### Good Output 2

![Good Output 2](demo/good_output_2.jpg)

## 4) 데모: 만화 느낌이 잘 표현되지 않은 예시 (2개)

> 아래 2칸에 결과 이미지 파일을 넣어주세요.

### Bad Output 1

![Bad Output 1](demo/bad_output_1.jpg)

### Bad Output 2

![Bad Output 2](demo/bad_output_2.jpg)

## 5) 알고리즘 한계점

1. **저화질 입력 이미지 문제**  
   원본 사진의 해상도가 낮거나 압축 노이즈가 많으면, 에지 추출 과정에서 경계가 뭉개지거나 과검출되어 만화 변환 결과의 윤곽선이 실제보다 두껍고 거칠게 표현될 수 있습니다.

2. **텍스처 손실**  
   색을 평탄화하는 과정에서 피부, 머리카락, 잔디 같은 미세 질감이 줄어들어 디테일이 부족해 보일 수 있습니다.

3. **파라미터 민감도**  
   `adaptive_block_size`, `adaptive_c`, `bilateral_iters` 값에 따라 선의 강도와 색감이 크게 달라지므로, 이미지마다 적절한 값이 다를 수 있습니다.

4. **장면 일반화 한계**  
   조명이 극단적이거나 배경이 복잡한 이미지에서는 일부 영역만 과도하게 강조되어 결과 품질이 불균일해질 수 있습니다.

## 6) 파일 구성

- `cartoon_render.py`: 만화 렌더링 코드
- `README.md`: 프로그램 설명, 데모, 한계점

