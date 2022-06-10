## 🥃 WeSuki 🥃 

![image](https://user-images.githubusercontent.com/99862931/172769705-45084dbc-6d42-431f-a1f5-9a70adf272fb.png)

![image](https://user-images.githubusercontent.com/99862931/172769788-51c804c3-bb96-460b-a916-a8df2e58c95c.png)




##  1. 프로젝트 개요



> **개발 목표** : 사용자들에게 개인 취향을 반영하여 사용자 맞춤의 새로운 위스키를 추천하는 서비스를 구현


## 2. 서비스 Demo

### 2.1 Demo - Beginners (입문자, 위스키 경험이 없는 유저)

![beginner_pick](https://user-images.githubusercontent.com/69205130/172971804-9cb62391-4c38-492e-b5bf-387223f64e50.gif)

**서비스를 시작하고 경험이 없다를 선택하면, 가장 먼저 맛에 대한 본인의 선호도를 slider의 형식으로 선택합니다.**

**여러 개의 설문이 끝나면, 해당 설문에 대한 본인이 답한 선택을 확인할 수 있고, 추천을 받을지 다시 선택을 할지 고를 수 있습니다.**

**'네'를 선택하면 추천 결과 화면으로 이어집니다.**


![beginner_result](https://user-images.githubusercontent.com/69205130/172971812-ff42b4d0-3d3e-41b1-8f2f-6cc21ec126e3.gif)

**입문자의 추천 결과 화면입니다.**

**본인이 선택한 맛에 대한 선호도를 바탕으로 학습한 추천 결과를 "취향 저격 베스트 위스키"에서 랭킹 순서로 확인 가능합니다.**

**"현재 가장 인기가 많은 위스키"에는 MetaCrtic 평점, 리뷰 갯수 등을 활용해 인기도를 선정한 결과를 확인할 수 있습니다."**

<br>

### 2.2 Demo - Experienced (위스키 경험이 있는 유저)

![ex_pick](https://user-images.githubusercontent.com/69205130/172971824-ccf6fa50-74c1-41e6-9927-b3dcacad9118.gif)

**서비스를 시작하고 경험이 있다를 선택하면, 위스키 경험이 없는 입문자 유저와 마찬가지로 맛에 대한 본인의 선호도를 slider의 형식으로 선택합니다.**

**여러 개의 설문이 끝나면, 해당 설문에 대한 본인이 답한 선택을 확인할 수 있습니다**

**입문자와는 달리, 위스키 경험이 이미 있는 유저들은 마셔본 위스키들을 선택하고(search 가능) 각 경험에 대한 평가를 👍 과 👎 을 통해 선택할 수 있습니다.**

**경험 선택을 확정지으면, 추천 결과 화면으로 이어집니다.**


![ex_result](https://user-images.githubusercontent.com/69205130/172971836-e799cb2d-aa15-40f7-816c-c0b45bd1a8e8.gif)

**경험자의 추천 결과 화면입니다.**

**본인이 선택한 위스키 경험을 바탕으로 학습한 추천 결과를 "경험을 바탕으로 추천해드리는 위스키"에서 확인 할 수 있습니다. (입문자 추천 결과와 차별점)**

**본인이 선택한 맛에 대한 선호도를 바탕으로 학습한 추천 결과를 "취향 저격 베스트 위스키"에서 랭킹 순서로 확인 가능합니다.**

**"현재 가장 인기가 많은 위스키"에는 MetaCrtic 평점, 리뷰 갯수 등을 활용해 인기도를 선정한 결과를 확인할 수 있습니다."**

<br>

## Members

|                                                  [김연요](https://github.com/arkdusdyk)                                                   |                                                                          [김진우](https://github.com/Jinu-uu)                                                                           |                                                 [박정훈](https://github.com/iksadNorth)                                                  |                                                                        [이호진](https://github.com/ili0820)                                                                         |                                                                         [최준혁](https://github.com/JHchoiii)                                                                         |
| :-------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------: |
| [![Avatar](https://avatars.githubusercontent.com/u/69205130?s=400&u=a14d779da6a9023a45e60e44072436d356a9461c&v=4)](https://github.com/arkdusdyk) | [![Avatar](https://avatars.githubusercontent.com/u/82719310?v=4)](https://github.com/Jinu-uu) | [![Avatar](https://avatars.githubusercontent.com/u/66674140?v=4)](https://github.com/iksadNorth) | [![Avatar](https://avatars.githubusercontent.com/u/65278309?v=4)](https://github.com/ili0820) | [![Avatar](https://avatars.githubusercontent.com/u/99862931?v=4)](https://github.com/JHchoiii) |
|  | | |  |  |

---

## 3. 서비스 아키텍쳐

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

## 4. DataSet


### 1) [Whiskybase](https://whiskybase.com)
: 약 54만개 이상의 유저 interaction data들을 crawling -> whisky, user (pseudonymized), rating, price, url 링크의 형태로 저장
 ![image](https://user-images.githubusercontent.com/99862931/172775752-cddfc09b-015a-4e80-9391-c1b26439de0b.png)


### 2) [Flavor Cluster Data](https://whiskyanalysis.com)
 : 위스키는 특히나 맛(Flavor)이 중요한 요소 - 위스키의 맛을 기반으로 전문가들에 의해 clustering

![image](https://user-images.githubusercontent.com/99862931/172775587-ccd5afd5-9810-42fa-ac22-b4e596e54b19.png)



---

## 5. Product Serving



**무경험자 flow chart**
- Model : 인기도 기반, 코사인 유사도

![image](https://user-images.githubusercontent.com/99862931/173078329-497a306b-cc2f-4443-9027-585a0d961e51.png)


**유경험자 flow chart**
- Model : RecVAE

![image](https://user-images.githubusercontent.com/99862931/173078121-f8857a0b-efe2-4285-a84a-ab0add3359b8.png)

## 6. ****How to Run****

```
make -j 2 run_app
```

## 7. Result & Conclusion

**위스키를 이미 즐기는 사람 뿐만 아니라 새로 입문하는 유저에게
취향에 맞는 위스키를 추천해주는 서비스 “We Suki“ 를 구축함**

[확장성 & 기대효과] 
- 추천한 결과를 저장하여 재학습을 통해 더 좋은 성능의 추천 제공

- 위스키에 국한되지 않고 타 주류/도메인에 대한 추천으로도 확장 가능

- 위스키 시장의 활성화






