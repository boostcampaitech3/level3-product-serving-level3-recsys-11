
import streamlit as st
import sys
current_module = sys.modules[__name__]

import pandas as pd
import json
import requests
from collections import namedtuple
requests_tuple = namedtuple('requests_tuple', 'text')


# button을 위해 설계 & 상수 정의 함수
def save(**kwarg):
    for k,v in kwarg.items():
        st.session_state[k] = v

# 위스키 이미지 출력
def img_whisky(name:str):
    img_url = requests.get("http://127.0.0.1:8001/image/"+ name).text[1:-1]
    st.components.v1.html(f'<img src="{img_url}" style="height:220px;" />', height=240)
    st.caption(name)

# 위스키 정보 출력
def info_whisky(name:str):
    result=requests.get("http://127.0.0.1:8001/info/"+ name).json()
    price=result[0]
    links=result[1]
    st.write(f'**[{name}]({links})**')
    st.text(f'{price[0]}')
    st.text(f'{price[1]}')

# 위스키 평가표 출력
def radio_whisky(name:str):
    like = st.radio('평가', ('👍', '👎'), key=name)
    dict_emoji = {'👍':True, '👎':False}
    like = dict_emoji[like]
    
    st.session_state['whisky_list'].update({name: like})

# unit 무한 제공 iterator
# Num : 한 줄에 몇 개의 item이 들어갈지 결정하는 매개변수
def units(Num):
    while True:
        with st.container():
            for col in st.columns(Num):
                yield col
           
# cells 함수가 내놓는 공간에 차례로 정보를 기입시켜주는 함수.
# list_func : 한 unit에 기입할 정보를 차례대로 쌓아주면 됨. 
# 이 때, func은 name_whiskey를 매개변수로 받는 함수여야 한다.
def arrange_units(array_items, Num, list_func):
    array_cells_func = [(units(Num), func) for func in list_func]
    
    for item in array_items:
        for cell, func in array_cells_func:
            with next(cell):
                func(item)

# rating을 위한 unit
def survey_whisky(array_items, Num=5):
    arrange_units(array_items, Num, [img_whisky, radio_whisky])

# 출력을 위한 unit
def display_whisky(array_items, Num=5):
    if array_items:
        arrange_units(array_items, Num, [img_whisky, info_whisky])
    else:
        with st.columns([1.4,1,1])[1]:
            st.write('')
            st.text('조회 결과가 없음')
            st.write('')
            st.write('')
 
# 상수 초기값 정의
init = {
    'is_beginner': True,
    'Scene': 1,
    'tag_list': {},
    'counter': 0,
    'value': 0,
    'whisky_list': {}
}

# 상수 초기화
for k,v in init.items():
    if k not in st.session_state:
        st.session_state[k] = v

 
def Scene1():
    with st.columns([1,15])[1]:
        st.image('Frontend/img/환영합니다.jpg')
    st.title("")
    with st.columns([1,5])[1]:
        st.image('Frontend/img/나는_위스키를_마셔본_적이.jpg')
    st.title("")
    
    _, left, right = st.columns([1.5,2,2])
    with left:      
        st.button('있다!', on_click=save, kwargs={'is_beginner':False, 'Scene':2})
        
    with right:
        st.button('없다!', on_click=save, kwargs={'is_beginner':True, 'Scene':2})


def Scene2():
    key, val = None, None
    encode = {'매우 안좋아함':-1.0,'안좋아함':-0.5,'모름':0.0,'좋아함':0.5,'매우 좋아함':1.0, '그렇지 않음':-1.0, '그러함':1.0, 0:0.0}
    
    opt_list = ['매우 안좋아함','안좋아함','모름','좋아함','매우 좋아함']
    opt_bool = ['그렇지 않음', '그러함']
    
    if st.session_state['counter'] == 0:
        with st.columns([1, 0.2])[0]:
            st.image('Frontend/img/body.jpg')
        val=st.select_slider("",options =opt_list,key = "value", value='모름')
        key = 'body'
        val = encode[val]
    elif st.session_state['counter'] == 1:
        with st.columns([1,1.20])[0]:
            st.image('Frontend/img/sweet.jpg')
        val=st.select_slider("",options =opt_list,key = "value", value='모름') #단맛을 즐기시나요?
        key = 'sweet'
        val = encode[val]
    elif st.session_state['counter'] == 2:
        with st.columns([1,0.25])[0]:
            st.image('Frontend/img/sherry.jpg')
        val=st.select_slider("",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'sherry'
        val = encode[val]
    elif st.session_state['counter'] == 3:
        with st.columns([1,1.4])[0]:
            st.image('Frontend/img/malt.jpg')
        val=st.select_slider("",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'malt'
        val = encode[val]
    elif st.session_state['counter'] == 4:
        with st.columns([1,1.15])[0]:
            st.image('Frontend/img/aperitif.jpg')
        val=st.select_slider("",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'aperitif'
        val = encode[val]
    elif st.session_state['counter'] == 5:
        with st.columns([1,0.3])[0]:
            st.image('Frontend/img/smoky.jpg')
        val=st.select_slider("",options =opt_list,key = "value", value='모름') #훈연향을 좋아하시나요?
        key = 'smoky'
        val = encode[val]
    elif st.session_state['counter'] == 6:
        with st.columns([1,0.4])[0]:
            st.image('Frontend/img/pungent.jpg')
        val=st.select_slider("",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'pungent'
        val = encode[val]
    elif st.session_state['counter'] == 7:
        with st.columns([1,0.8])[0]:
            st.image('Frontend/img/fruity.jpg')
        val=st.select_slider("",options =opt_list,key = "value", value='모름') #과일을 좋아하시나요?
        key = 'fruity'
        val = encode[val]
    elif st.session_state['counter'] == 8:
        with st.columns([1,0.84])[0]:
            st.image('Frontend/img/honey.jpg')
        val=st.select_slider("",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'honey'
        val = encode[val]
    elif st.session_state['counter'] == 9:  
        with st.columns([1,0.7])[0]:
            st.image('Frontend/img/floral.jpg')
        val=st.select_slider("",options =opt_list,key = "value", value='모름') #꽃향기를 좋아하시나요?
        key = 'floral'
        val = encode[val]
    elif st.session_state['counter'] == 10:
        with st.columns([1,0.73])[0]:
            st.image('Frontend/img/spicy.jpg')
        val=st.select_slider("",options =opt_list,key = "value", value='모름') #매운 것을 잘 드시나요?
        key = 'spicy'
        val = encode[val]
    elif st.session_state['counter'] == 11:
        with st.columns([1,0.60])[0]:
            st.image('Frontend/img/medicinal.jpg')
        val=st.select_slider("",options =opt_list,key = "value", value='모름') #한약을 잘 드시나요?
        key = 'medicinal'
        val = encode[val]
    elif st.session_state['counter'] == 12:
        with st.columns([1,0.73])[0]:
            st.image('Frontend/img/nutty.jpg')
        val=st.select_slider("",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'nutty'
        val = encode[val]
    elif st.session_state['counter'] == 13:
        with st.columns([1,0.73])[0]:
            st.image('Frontend/img/winey.jpg')
        val=st.select_slider("",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'winey'
        val = encode[val]
    
    idx_max, idx_min = 13, 0
    def Next():
        if st.session_state['counter'] < idx_max:
            st.session_state['counter'] += 1
        else:
            save(Scene=3, counter=0)
        if key:
            st.session_state["tag_list"].update({key:val})
    
    def Previous():
        if st.session_state['counter'] > idx_min:
            st.session_state['counter'] -= 1
        else:
            pass
        if key:
            st.session_state["tag_list"].update({key:val})
    
    _, left, right = st.columns([1.5,2,2])
    with left:
        st.button("previous", on_click=Previous)
    with right:
        st.button("next", on_click=Next)
    

def Scene3():
    decode = {0.0:'모름',-1.0:'매우 안좋아함',-0.5:'안좋아함',0.5:'좋아함',1.0:'매우 좋아함'}
    
    st.sidebar.table(pd.Series(st.session_state["tag_list"], name='취향 선택').map(lambda x: decode[x]))
    
    with st.columns([1,5,1])[1]:
            st.image('Frontend/img/선택하신_취향으로_추천을_받으시겠습니까.jpg')
    
    st.title("")
    st.title("")
    
    _, left, right = st.columns([1.0,2,2])
    with left:
        Num = 6 if st.session_state['is_beginner'] else 4
        st.button('네', on_click=save, kwargs={'Scene':Num})
    
    with right:
        st.button('다시 시도', on_click=save, kwargs={'counter':0, 'Scene':2})
        
        
def Scene4():
    with st.columns([1,3,1])[1]:
        st.image('Frontend/img/마셔본_위스키들을_선택하고_평가해주세요.jpg')
        st.title('')
        result=requests.get('http://127.0.0.1:8001/whisky_datas').json()
        
        df_final=pd.Series(result)        
        whiskey = st.multiselect('검색창', df_final)

    with st.columns([1,3,1])[1]:
        st.title('')
        st.button('확인', on_click=save, kwargs={'Scene':5})
    
    if not whiskey:
        whiskey = []
    condition_word = df_final.isin(whiskey)
    df_with_condition = df_final[condition_word]
    
    survey_whisky(df_with_condition)
    
    whisky_list = st.session_state['whisky_list']
    st.session_state['whisky_list'] = {item:rating for item, rating in whisky_list.items() if item in whiskey}

    
def Scene5():
    encode = {True: '👍', False: '👎'}
    st.sidebar.table(pd.Series(st.session_state["whisky_list"], name='선호 여부').map(lambda x : encode[x]))
    
    with st.columns([1,5,1])[1]:
        st.image('Frontend/img/선택하신_취향과_위스키들로_추천을_받으시겠습니까.jpg')
    
    st.title("")
    st.title("")
    
    _, left, right = st.columns([1,2,2])
    with left:
        st.button('네', on_click=save, kwargs={'Scene':6})
    
    with right:
        st.button('다시 시도', on_click=save, kwargs={'Scene':4})
        
        
def Scene6():
    # sidebar
    opt_price = {'0원':0, '3만원':30000, '5만원':50000, '7만원':70000, '12만원':125000, '30만원':300000, '30만원+':1000000}
    price_low, price_high = st.sidebar.select_slider("", options =opt_price.keys(), value=('0원', '30만원+'))
    price_low, price_high = opt_price[price_low], opt_price[price_high]
    topk = st.sidebar.number_input('갯수', step=1, value=5, min_value=0)

    # API.
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("Frontend/img/추천_결과.jpg")
    with col3:
        st.write(' ')
    st.title("")
    st.title("")
    #model
    if not st.session_state['is_beginner']:
        whiskies_like=[]
        whiskies_hate=[]
        for k,v in st.session_state["whisky_list"].items():
            if v:
                whiskies_like.append(k)
            else:
                whiskies_hate.append(k)
    
        params={"whiskies_like":whiskies_like,"whiskies_hate":whiskies_hate,"price_low":price_low,"price_high":price_high,"topk":topk}
        result = requests.post("http://127.0.0.1:8001/recommend_m", json=params)
        
        if result.status_code==500:
            result = requests_tuple(text=json.dumps({'model': []}))
            
        result=json.loads(result.text)
    
        result_model=[]
        for i in result['model']:
            result_model.append(i['name'])

        st.image('Frontend/img/경험을_바탕으로_추천해드리는_위스키.jpg')
        display_whisky(result_model)

    #tag
    params={"tag_list":st.session_state['tag_list'],"price_low":price_low,"price_high":price_high,"topk":topk}
    result = requests.post("http://127.0.0.1:8001/recommend_t", json=params)
    
    if result.status_code==500:
        result = requests_tuple(text=json.dumps({'tag': []}))
    
    result=json.loads(result.text)

    st.title("")
    result_tag=[]
    for i in result['tag']:
        result_tag.append(i['name'])
    st.image('Frontend/img/취향_저격_베스트_위스키.jpg')
    display_whisky(result_tag)

    #popularity
    params={"price_low":price_low, "price_high":price_high, "topk":topk}
    result = requests.post("http://127.0.0.1:8001/recommend_p", json=params)
    
    if result.status_code==500:
        result = requests_tuple(text=json.dumps({'popularity': []}))
    
    result=json.loads(result.text)

    st.title("")
    result_pop=[]
    for i in result['popularity']:
        result_pop.append(i['name'])
    st.image('Frontend/img/현재_가장_인기가_많은_위스키.jpg')
    display_whisky(result_pop)
    
 
N = st.session_state['Scene']

# config
st.set_page_config(
     page_title="WeSuki",
     page_icon="Frontend/img/icon_logo.jpg",
     layout="centered",
     initial_sidebar_state="expanded",
 )

# Team Logo
with st.columns([1, 6, 1])[1]:
    st.image('Frontend/img/team_logo.jpg')

# Scene 활성화
run_scene = getattr(current_module, f'Scene{N}')
run_scene()

