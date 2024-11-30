import json
import random

data = []
existing_combinations = set()  # 이미 존재한 조합을 추적하기 위한 집합

pk_counter = 1

# 각 DepositOption에 대해 랜덤한 유저들 연결
for option_id in range(1, 155):  # DepositOption ID는 1부터 156까지
    # 1~5명의 유저와 랜덤하게 연결 (유저는 100명)
    user_ids = random.sample(range(1, 101), random.randint(1, 5))  # 랜덤한 1~5명 유저를 선택
    
    for user_id in user_ids:
        combination = (option_id, user_id)  # 조합 생성
        
        # 이미 존재하는 조합인 경우 건너뛰기
        if combination in existing_combinations:
            continue

        # 조합이 존재하지 않으면 데이터를 추가
        data.append({
            "model": "finance.depositoption_registered_user",  # 모델 경로
            "pk": pk_counter,
            "fields": {
                "depositoption": option_id,  # DepositOption의 ID
                "user": user_id  # User의 ID
            }
        })
        pk_counter += 1
        existing_combinations.add(combination)  # 조합을 기존 집합에 추가

# JSON 파일로 저장
with open("depositoption_registered_user.json", "w") as f:
    json.dump(data, f, indent=4)

print("depositoption_registered_user.json 생성 완료")

data = []
existing_combinations = set()  # 이미 존재한 조합을 추적하기 위한 집합

pk_counter = 1

# 각 DepositOption에 대해 랜덤한 유저들 연결
for option_id in range(1, 160):  # DepositOption ID는 1부터 156까지
    # 1~5명의 유저와 랜덤하게 연결 (유저는 100명)
    user_ids = random.sample(range(1, 101), random.randint(1, 5))  # 랜덤한 1~5명 유저를 선택
    
    for user_id in user_ids:
        combination = (option_id, user_id)  # 조합 생성
        
        # 이미 존재하는 조합인 경우 건너뛰기
        if combination in existing_combinations:
            continue

        # 조합이 존재하지 않으면 데이터를 추가
        data.append({
            "model": "finance.savingoption_registered_user",  # 모델 경로
            "pk": pk_counter,
            "fields": {
                "savingoption": option_id,  # DepositOption의 ID
                "user": user_id  # User의 ID
            }
        })
        pk_counter += 1
        existing_combinations.add(combination)  # 조합을 기존 집합에 추가

# JSON 파일로 저장
with open("savingoption_registered_user.json", "w") as f:
    json.dump(data, f, indent=4)

print("savingoption_registered_user.json 생성 완료")