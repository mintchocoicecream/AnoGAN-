# AnoGAN
## Tensorflow Deeplearning Final Project
#### *Hyunjeong Seo, Hyunsuk Choi, Taekwan Kim*
* AnoGAN 알고리즘을 이용한 자동차 핸들 오류 검출 프로그램

참고 : https://github.com/amandaberg/GANanomalyDetection.git

## Requirement
- Python 3.7
- numpy >= 1.13.3
- scipy >= 1.0.0
- tensorflow-gpu >= 1.6.0
- moviepy >= 0.2.3.2
- Pillow >= 3.1.1
- lmdb >= 0.93
- opencv-python >= 3.4.0.12
- cryptography >= 2.1.4
- h5py >= 2.7.1
- six >= 1.11.0

## AnoGAN
- AnoGAN Train : AnoGAN Model train.py
- AnoGAN Test : AnoGAN config.py 주석변경후 테스트

## Dataset
- Train datasets : train -- 제네시스 G80 핸들 통화버튼 & 통화종료버튼 각 44장
- Test datasets : validation -- 제니시스 G80 핸들 정상이미지 & 비정상이미지

## Changes
- tfutil.py -- AnomalyDetection <- AnomalyScore추가

## Output
- Program -- 오류검출프로그램

- Login
<img src="https://user-images.githubusercontent.com/64584574/192470992-6cbca6c1-ef13-4f45-b681-b14d6a915509.PNG"  width="700">

- Main Program
<img src="https://user-images.githubusercontent.com/64584574/192471007-f1966ea9-ca8f-4510-9b69-bb6a6c365934.PNG"  width="700">


- UI -- QT Designer
