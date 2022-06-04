# %%
import streamlit as st
import sys
current_module = sys.modules[__name__]

import pandas as pd
import numpy as np
from deprecated import deprecated


# %%
# 가격 환산.
dict_range_cost = {
    "$":        ('3만원 이하',),
    "$$":       ('3만원 이상', '5만원 이하'),
    "$$$":      ('5만원 이상', '7만원 이하'),
    "$$$$":     ('6만원 이상', '12만원 이하'),
    "$$$$$":    ('12만원 이상', '30만원 이하'),
    "$$$$$+":   ('30만원 이상', ),
    }

# button을 위해 설계 & 상수 정의 함수
def save(**kwarg):
    for k,v in kwarg.items():
        st.session_state[k] = v

# 위스키 이미지 출력
def img_whisky(name:str):
    df = st.session_state['df_final']
    
    img_url = df[df.Whiskey.isin([name])].images.iloc[0]
    st.image(img_url, caption=name, width=128)

# 위스키 정보 출력
def info_whisky(name:str):
    condition = st.session_state['df_final'].Whiskey == name
    
    price = st.session_state['df_final'].Cost
    Type = st.session_state['df_final'].Class
    links = st.session_state['df_final'].links
    
    price = price[condition].iloc[0]
    price = dict_range_cost[price]
    
    st.write(f'**[{name}]({links[condition].iloc[0]})**')
    st.text(f'{price[0]}')
    st.text(f'{price[1]}')

# 위스키 평가표 출력
def radio_whisky(name:str):
    like = st.radio('평가', ('👍', '👎'), key=name)
    dict_emoji = {'👍':True, '👎':False}
    like = dict_emoji[like]
    
    st.session_state['whisky_list'].update({name: like})

# 현실적인 문제를 고려한 Unit
@deprecated(reason="검색 구조를 바꿈.")
def survey_whisky(Num:int, df_ind):
    try:
        col(Num, lambda idx : img_whisky(df_ind[idx]))
        col(Num, lambda idx : radio_whisky(df_ind[idx]))
    except:
        with st.columns([1,3,1])[1]:
            st.subheader('조회 결과 없음.')

# 현실적인 문제를 고려한 Unit
@deprecated(reason="검색 구조를 바꿈.")
def display_whisky(Num:int, df_ind):
    try:
        col(Num, lambda idx : img_whisky(df_ind[idx]))
        col(Num, lambda idx : info_whisky(df_ind[idx]))
    except:
        with st.columns([1,3,1])[1]:
            st.subheader('조회 결과 없음.')
            
# 현실적인 문제를 고려한 Unit
def survey_whisky_with_df(df, Num=10):
    cells_upper_iter = cells()
    cells_lower_iter = cells()
    for idx, item in enumerate(df):
        with next(cells_upper_iter):
            img_whisky(item)
        with next(cells_lower_iter):
            radio_whisky(item)
        if idx + 1 >= Num:
            break

# 현실적인 문제를 고려한 Unit
def display_whisky_with_df(df, Num=10):
    cells_upper_iter = cells()
    cells_lower_iter = cells()
    for idx, item in enumerate(df):
        with next(cells_upper_iter):
            img_whisky(item)
        with next(cells_lower_iter):
            info_whisky(item)
        if idx + 1 >= Num:
            break

# unit 가로 나열
def col(Num:int=5, func=lambda idx:None):
    with st.container():
        for ind, col in enumerate(st.columns(Num)):
            with col:
                func(ind)

# unit 무한 제공 iterator
def cells(Num=5):
    while True:
        with st.container():
            for ind, col in enumerate(st.columns(Num)):
                if ind >= Num: break
                yield col

# %%
# 상수 초기값 정의
init = {
    'is_beginner': True,
    'Scene': 1,
    'tag_list': {},
    'counter': 0,
    'value': 0,
    'whisky_list': {},
    'df_final': pd.read_csv('../Dataset/total_df.csv', sep='$'),
}

# 상수 초기화
for k,v in init.items():
    if k not in st.session_state:
        st.session_state[k] = v

# %%
def Scene1():
    with st.columns([1.5,3])[1]:
        # st.title(':wine_glass: 환영합니다!! :wine_glass:')
        st.title('환영합니다!!')
    st.title("")
    with st.columns([1.1,3])[1]:
        st.subheader('나는 위스키를 마셔본 적이')
    
    st.title("")
    
    _, left, right = st.columns([1.5,2,2])
    with left:      
        st.button('있다!', on_click=save, kwargs={'is_beginner':False, 'Scene':2})
        
    with right:
        st.button('없다!', on_click=save, kwargs={'is_beginner':True, 'Scene':2})


def Scene2():
    key, val = None, None
    encode = {'모름':0.50,'매우 안좋아함':0.0,'안좋아함':0.25,'좋아함':0.75,'매우 좋아함':1.0, True:1.0, False:0.0, '그렇지 않음':1.0, '그러함':0.0}
    
    opt_list = ['매우 안좋아함','안좋아함','모름','좋아함','매우 좋아함']
    opt_bool = ['그렇지 않음', '그러함']
    
    if st.session_state['counter'] == 0:
        # with st.expander("바디감이란?"):
        #     st.write("바디감은 알코올, 음료의 무게감이라고도 표현합니다.")
        #     st.write("음료의 진하기라고도 표현하며, 비교를 하자면")
        #     st.write("안동소주:바디감 강함, 진로:바디감 약함 입니다.")
        val=st.select_slider("바디감 있는게 좋으신가요?",options =opt_list,key = "value", value='모름')
        key = 'body'
        val = encode[val]
    elif st.session_state['counter'] == 1:
        val=st.select_slider("단맛을 즐기시나요?",options =opt_list,key = "value", value='모름') #단맛을 즐기시나요?
        key = 'sweet'
        val = encode[val]
    elif st.session_state['counter'] == 2:
        # val=st.checkbox("와인을 좋아하시나요?",key = "value") #와인을 좋아하시나요?
        val=st.select_slider("와인을 즐기시나요?",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'sherry'
        val = encode[val]
    elif st.session_state['counter'] == 3:
        # val=st.checkbox("곡물을 좋아하시나요?",key = "value") #곡물을 좋아하시나요?
        val=st.select_slider("곡물을 즐기시나요?",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'malt'
        val = encode[val]
    elif st.session_state['counter'] == 4:
        # val=st.checkbox("식전주를 즐겨드시나요?",key = "value") #식전주를 즐겨드시나요?
        val=st.select_slider("식전주을 즐기시나요?",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'aperitif'
        val = encode[val]
    elif st.session_state['counter'] == 5:
        val=st.select_slider("훈연향을 좋아하시나요?",options =opt_list,key = "value", value='모름') #훈연향을 좋아하시나요?
        key = 'smoky'
        val = encode[val]
    elif st.session_state['counter'] == 6:
        # val=st.checkbox("양파향(?)을 좋아하시나요?",key = "value") #양파향(?)을 좋아하시나요?
        val=st.select_slider("양파향을 즐기시나요?",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'pungent'
        val = encode[val]
    elif st.session_state['counter'] == 7:
        val=st.select_slider("과일을 좋아하시나요?",options =opt_list,key = "value", value='모름') #과일을 좋아하시나요?
        key = 'fruity'
        val = encode[val]
    elif st.session_state['counter'] == 8:
        # val=st.checkbox("꿀을 좋아하시나요?",key = "value") #꿀을 좋아하시나요?
        val=st.select_slider("꿀을 좋아하시나요?",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'honey'
        val = encode[val]
    elif st.session_state['counter'] == 9:  
        val=st.select_slider("꽃향기를 좋아하시나요?",options =opt_list,key = "value", value='모름') #꽃향기를 좋아하시나요?
        key = 'floral'
        val = encode[val]
    elif st.session_state['counter'] == 10:
        val=st.select_slider("매운 것을 잘 드시나요?",options =opt_list,key = "value", value='모름') #매운 것을 잘 드시나요?
        key = 'spicy'
        val = encode[val]
    elif st.session_state['counter'] == 11:
        val=st.select_slider("한약을 잘 드시나요?",options =opt_list,key = "value", value='모름') #한약을 잘 드시나요?
        key = 'medicinal'
        val = encode[val]
    elif st.session_state['counter'] == 12:
        # val=st.checkbox("견과류 향기를 좋아하시나요?",key = "value")  #견과류 향기를 좋아하시나요?
        val=st.select_slider("견과류 향기를 좋아하시나요?",options =opt_bool,key = "value", value='그렇지 않음')
        key = 'nutty'
        val = encode[val]
    elif st.session_state['counter'] == 13:
        # val=st.checkbox("포도주 좋아하시나요?",key = "value") #포도주 좋아하시나요?
        val=st.select_slider("포도주 좋아하시나요?",options =opt_bool,key = "value", value='그렇지 않음')
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
    
    # st.sidebar.table(pd.Series(st.session_state["tag_list"], name='취향 점수'))
    
    _, left, right = st.columns([1.5,2,2])
    with left:
        st.button("previous", on_click=Previous)
    with right:
        st.button("next", on_click=Next)
    

def Scene3():
    st.sidebar.table(pd.Series(st.session_state["tag_list"], name='취향 점수'))
    
    with st.columns([1,3,1])[1]:
        st.title('답변 주신 취향을 확정지을까요??')
    
    st.title("")
    
    _, left, right = st.columns([1.0,2,2])
    with left:
        Num = 6 if st.session_state['is_beginner'] else 4
        st.button('네', on_click=save, kwargs={'Scene':Num})
    
    with right:
        st.button('다시 시도', on_click=save, kwargs={'counter':0, 'Scene':2})
        
        
def Scene4():
    df_final = st.session_state['df_final']

    with st.columns([1,3,1])[1]:
        st.title('당신의 경험을 이야기해주세요!')
        st.title('')
        whiskey = st.multiselect('검색창', df_final.Whiskey)
    
    with st.columns([1,3,1])[1]:
        st.title('')
        st.button('확인', on_click=save, kwargs={'Scene':5})
    
    if not whiskey:
        whiskey = []
        
    condition_word = df_final.Whiskey.isin(whiskey)
    df_with_condition = df_final[condition_word].Whiskey

    survey_whisky_with_df(df_with_condition)
    
    whisky_list = st.session_state['whisky_list']
    st.session_state['whisky_list'] = {item:rating for item, rating in whisky_list.items() if item in whiskey}
    
    # st.sidebar.write(st.session_state["whisky_list"])
    # st.sidebar.table(pd.Series(st.session_state["whisky_list"], name='선호 여부'))

    
def Scene5():
    encode = {True: '👍', False: '👎'}
    st.sidebar.table(pd.Series(st.session_state["whisky_list"], name='선호 여부').map(lambda x : encode[x]))
    
    with st.columns([1,3,1])[1]:
        st.title('답변 주신 위스키들을 확정지을까요??')
    
    st.title("")
    
    _, left, right = st.columns([1,2,2])
    with left:
        st.button('네', on_click=save, kwargs={'Scene':6})
    
    with right:
        st.button('다시 시도', on_click=save, kwargs={'Scene':4})
        
        
def Scene6():
    from utils import Collector, Greeter

    # sidebar
    price_low, price_high = st.sidebar.slider('가격 [원화 기준]', 0, 1000000, (0, 1000000), step=5000)
    topk = st.sidebar.number_input('갯수', step=1, value=5, min_value=0, max_value=6)
    
    # 객체 로딩.
    for_newbie = Greeter()
    for_expert = Collector()
    
    
    # 단순 인기도 기반 추천
    df_pop = for_expert._popularity(topk)
    
    
    # 태그 기반 추천
    result_cluster, result_df_cluster = for_newbie.find_cluster(st.session_state['tag_list'])
    result_filter_by_price = for_newbie.filter_by_price(result_df_cluster, price_low, price_high)
    result_sort_by_popularity = for_newbie.sort_by_popularity(result_filter_by_price, topk=10)
    
    df_tag_pop = result_sort_by_popularity.Whiskey.iloc
    
    
    # 추천 시스템 기반 추천
    history = st.session_state['whisky_list']
    for_expert.goods = [item for item, rating in history.items() if rating]
    for_expert.poors = [item for item, rating in history.items() if not rating]
    
    df_recvae = for_expert._recvae_topk(topk)
    
    
    # 표현 구간.
    Num = topk
    st.title('인기 상품')
    display_whisky(Num, df_pop)
    
    st.title('내 취향에 맞는 상품')
    display_whisky(Num, df_tag_pop)

    if not st.session_state['is_beginner']:
        st.title('나에게 맞는 상품')
        display_whisky(Num, df_recvae)

    
# %%
N = st.session_state['Scene']

# config
st.set_page_config(
     page_title="WeSuki",
     page_icon="img/icon_logo.jpg",
     layout="centered",
     initial_sidebar_state="expanded",
 )

# Team Logo
with st.columns([1, 6, 1])[1]:
    st.image('img/team_logo.jpg')

# Scene 활성화
run_scene = getattr(current_module, f'Scene{N}')
run_scene()

# for debug
# st.title('')
# k = st.text_input(f'Scene{N}')
# st.button('warp', on_click=save, kwargs={'Scene':k})
# st.session_state

# %%
