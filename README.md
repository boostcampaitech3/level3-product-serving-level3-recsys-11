## 🥃 WeSuki 🥃 

![image](https://user-images.githubusercontent.com/99862931/172769705-45084dbc-6d42-431f-a1f5-9a70adf272fb.png)

![image](https://user-images.githubusercontent.com/99862931/172769788-51c804c3-bb96-460b-a916-a8df2e58c95c.png)




##  1. 프로젝트 개요


> **문제 정의**: 

> **개발 목표** : 사용자들에게 개인 취향을 반영하여 사용자 맞춤의 새로운 위스키를 추천하는 서비스

## Demo

- 무 경험자



###
- 유 경험자
![image](https://user-images.githubusercontent.com/99862931/172771286-7f3c29fc-1501-4188-9a78-ec78bb72df02.png)


## Members

|                                                  [김연요](https://github.com/arkdusdyk)                                                   |                                                                          [김진우](https://github.com/Jinu-uu)                                                                           |                                                 [박정훈](https://github.com/iksadNorth)                                                  |                                                                        [이호진](https://github.com/ili0820)                                                                         |                                                                         [최준혁](https://github.com/JHchoiii)                                                                         |
| :-------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------: |
| [![Avatar](https://avatars.githubusercontent.com/u/69205130?s=400&u=a14d779da6a9023a45e60e44072436d356a9461c&v=4)](https://github.com/arkdusdyk) | [![Avatar](https://avatars.githubusercontent.com/u/82719310?v=4)](https://github.com/Jinu-uu) | [![Avatar](https://avatars.githubusercontent.com/u/66674140?v=4)](https://github.com/iksadNorth) | [![Avatar](https://avatars.githubusercontent.com/u/65278309?v=4)](https://github.com/ili0820) | [![Avatar](https://avatars.githubusercontent.com/u/99862931?v=4)](https://github.com/JHchoiii) |
|  | | |  |  |

---

## 2️. 서비스 아키텍쳐

### 1) Project Tree
```bash
code
├── 📁 Backend
│   ├── 💾 __main__.py 
│   └── 💾 main.py 
│   
├── 📁 Dataset
│   ├── 📁 whiskey_with_taste
│   │   └──  ⋮
│   ├── 💾 README.md
│   ├── 💾 concat.ipynb
│   └── ⋮
│
├── 📁 Frontend
│   ├── 📁 img
│   │   └──  ⋮
│   └── 💾 main.py
│
├── 📁 Model
│   ├── 📁 __pycache__
│   │   └──  ⋮
│   ├── 📁 config
│   │   └──  ⋮
│   ├── 📁 dataset/whiskey_with_taste
│   │   └──  ⋮
│   ├── 📁 model_saved
│   │   └──  ⋮
│   ├── 💾 config.yaml   
│   ├── 💾 preprocessing.py
│   ├── 💾 train.py
│   └── 💾 utils.py
│
├── 📁 log/RecVAE
│   └── 📁 RecVAE
│        └──  ⋮
│
├── 💾 Makefile
└── 💾 README.md
```

### 2) System Architecture

![image](https://user-images.githubusercontent.com/99862931/172770644-c334dc94-fa7a-4818-a13e-748172fec4ba.png)



---

## 3️. DataSet


### 1) [Whiskybase](https://whiskybase.com)
: 약 54만개 이상의 유저 interaction data들을 crawling -> whisky, user (pseudonymized), rating, price, url 링크의 형태로 저장
 ![image](https://user-images.githubusercontent.com/99862931/172775752-cddfc09b-015a-4e80-9391-c1b26439de0b.png)


### 2) [Flavor Cluster Data](https://whiskyanalysis.com)
 : 위스키는 특히나 맛(Flavor)이 중요한 요소 - 위스키의 맛을 기반으로 전문가들에 의해 clustering

![image](https://user-images.githubusercontent.com/99862931/172775587-ccd5afd5-9810-42fa-ac22-b4e596e54b19.png)



---

## 4️. Modeling

### 1) 무 경험자

### 2) 유 경험자


---

## 5️. Product Serving

### 1) SW 구성


### 2) FrontEnd (Streamlit)

- 사용자 인터페이스 제공 : 이미지 업로드, 크롭, 설문, 전시 등
- 서비스 결과 전시 : 제품 유형, 유사 제품 이미지 등

### 3) BackEnd (FastAPI)

- Model 과 FrontEnd 를 연결
- Client로부터 데이터를 수신하여 Inference 모듈을 호출
- Inference 모듈로부터 추론 결과를 수신하여 Client로 전송



## 6️. ****How to Run****


### run
```
make -j 2 run_app

```
## 7. 후속 개발
- DB 추가
- 클라우드
- 추천 결과에 대한 유저피드백 저장후 


## 8️. Reference

