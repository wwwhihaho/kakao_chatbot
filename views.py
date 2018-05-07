from pyfasttext import FastText
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pytz import timezone
import datetime, json, sys, re, random
import pandas as pd


df_meal = pd.read_csv("/home/ubuntu/Django/app/meal.csv")
df_answer = pd.read_csv("/home/ubuntu/Django/fasttext/kakao - Answer.csv")["answer"].tolist()
df_food = pd.read_csv("/home/ubuntu/Django/fasttext/kakao - foodList.csv")["foodList"].tolist()
model = FastText('/home/ubuntu/Django/app/train.bin')

# 크롤링한 pandas 테이블 로드
def get_lunch(week_num):
    return str("점심\n-------------------------------\n") + \
           str([df_meal[df_meal["weekday"] == week_num].reset_index().lunch[i] for i in range(len(df_meal[df_meal["weekday"] == week_num].lunch))]) \
           .replace("[","").replace("]","").replace("'","").replace("%!%, ","").replace(", ","\n-------------------------------\n")

def get_dinner(week_num):
    return str("저녁\n-------------------------------\n") + \
           str([df_meal[df_meal["weekday"] == week_num].reset_index().dinner[i] for i in range(len(df_meal[df_meal["weekday"] == week_num].dinner))]) \
           .replace("[","").replace("]","").replace("'","").replace("%!%, ","").replace(", ","\n-------------------------------\n").replace("%!%","")

# 대화용 classifier
def classifier(sentence):
    try:
        print(int(model.predict_proba_single(sentence)[0][0]))
    except IndexError:
        print("알맞은 답변이 없습니다")
        return "잘 못알아들었어요"
    else:
        return df_answer[int(model.predict_proba_single(sentence)[0][0])]

# 초기화면으로 키보드 함수
def ret_proc(output):
    return JsonResponse({
            'message': {
                'text': output
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['뭐냥과 대화하기', '웰스토리 메뉴', '한컴 메뉴']
            }
        })

# 점심, 저녁 여부
def meal_proc(output):
    return JsonResponse({
            'message': {
                'text': output
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['점심', '저녁']
            }
        })

# 기본 키보드
def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['뭐냥과 대화하기', '웰스토리 메뉴', '한컴 메뉴']
    })

# 답변셋
@csrf_exempt
def answer(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']
    user_key = received_json_data['user_key']
    content_type = received_json_data['type']

    print(datacontent)

# 대화
    if (datacontent == "뭐냥과 대화하기") and (content_type=="buttons"):
        return JsonResponse({
            'message': {
                'text': "채팅을 시작합니다\n 종료를 원하시면 `종료`라고 적어주세요"
            },
            'keyboard': {
                'type': 'text'
            }
        })
    
    elif ("종료" in datacontent) and (content_type=='text'):
        return JsonResponse({
            'message': {
                'text': '채팅을 종료합니다.'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['뭐냥과 대화하기', '웰스토리 메뉴', '한컴 메뉴']
            }
        })

    elif ("추천" in datacontent) and (content_type=='text'):
        random_food = df_food[random.randint(0,len(df_food))] + " 먹으러 가는거 어떠냥?"
        return JsonResponse({
            'message': {
                'text': random_food
            },
            'keyboard': {
                'type': 'text'
            }
        })


# 한컴 답변
    elif "한컴" in datacontent:
        return ret_proc("https://m.facebook.com/ottimofood/")

# 웰스토리 답변 
    elif datacontent == '웰스토리 메뉴':
        return JsonResponse({
                'message': {
                    'text': '웰스토리 메뉴를 선택하셨군요\n확인하려는 요일을 선택해주세요'
                },
                'keyboard': {
                    'type': 'buttons',
                    'buttons': ['월요일', '화요일', '수요일', '목요일', '금요일'] 
                }
            })

# 월요일
    elif datacontent == "월요일 점심":
        return JsonResponse({
            'message': {
                'text': get_lunch(1)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['월요일 점심', '월요일 저녁', '처음으로']
            }
        })

    elif datacontent == "월요일 저녁":
        return JsonResponse({
            'message': {
                'text': get_dinner(1)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['월요일 점심', '월요일 저녁', '처음으로']
            }
        })

    elif datacontent == '월요일':
        return JsonResponse({
            'message': {
                'text': '월요일, 점심인가요? 저녁인가요?(하하)'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['월요일 점심', '월요일 저녁', '처음으로']
            }
        })


# 화요일
    elif datacontent == '화요일':
        return JsonResponse({
            'message': {
                'text': '화요일, 점심인가요? 저녁인가요?(하하)'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['화요일 점심', '화요일 저녁', '처음으로']
            }
        })

    elif datacontent == "화요일 점심":
        return JsonResponse({
            'message': {
                'text': get_lunch(2)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['화요일 점심', '화요일 저녁', '처음으로']
            }
        })

    elif datacontent == "화요일 저녁":
        return JsonResponse({
            'message': {
                'text': get_dinner(2)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['화요일 점심', '화요일 저녁', '처음으로']
            }
        })

# 수요일
    elif datacontent == '수요일':
        return JsonResponse({
            'message': {
                'text': '수요일, 점심인가요? 저녁인가요?(하하)'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['수요일 점심', '수요일 저녁', '처음으로']
            }
        })

    elif datacontent == "수요일 점심":
        return JsonResponse({
            'message': {
                'text': get_lunch(3)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['수요일 점심', '수요일 저녁', '처음으로']
            }
        })

    elif datacontent == "수요일 저녁":
        return JsonResponse({
            'message': {
                'text': get_dinner(3)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['수요일 점심', '수요일 저녁', '처음으로']
            }
        })

# 목요일
    elif datacontent == '목요일':
        return JsonResponse({
            'message': {
                'text': '목요일, 점심인가요? 저녁인가요?(하하)'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['목요일 점심', '목요일 저녁', '처음으로']
            }
        })

    elif datacontent == "목요일 점심":
        return JsonResponse({
            'message': {
                'text': get_lunch(4)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['목요일 점심', '목요일 저녁', '처음으로']
            }
        })

    elif datacontent == "목요일 저녁":
        return JsonResponse({
            'message': {
                'text': get_dinner(4)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['목요일 점심', '목요일 저녁', '처음으로']
            }
        })

# 금요일
    elif datacontent == '금요일':
        return JsonResponse({
            'message': {
                'text': '금요일, 점심인가요? 저녁인가요?(하하)'
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['금요일 점심', '금요일 저녁', '처음으로']
            }
        })

    elif datacontent == "금요일 점심":
        return JsonResponse({
            'message': {
                'text': get_lunch(5)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['금요일 점심', '금요일 저녁', '처음으로']
            }
        })

    elif datacontent == "금요일 저녁":
        return JsonResponse({
            'message': {
                'text': get_dinner(5)
            },
            'keyboard': {
                'type': 'buttons',
                'buttons': ['금요일 점심', '금요일 저녁', '처음으로']
            }
        })

# 처음으로
    elif datacontent == "처음으로":
        return ret_proc(datacontent)

    elif content_type=='text':
        return JsonResponse({
            'message': {
                'text': classifier(datacontent)
            },
            'keyboard': {
                'type': 'text'
            }
        })

# 기타
    else:
        return ret_proc(_else)


