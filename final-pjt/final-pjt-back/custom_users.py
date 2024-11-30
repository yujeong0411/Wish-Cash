import json
from random import randint, choice

data = []

for i in range(1, 101):
    data.append({
        "model": "accounts.user",
        "pk": i,
        "fields": {
            "username": f"testuser{i}",
            "password": "pbkdf2_sha256$260000$JwTkIzEAnbsX$uai9qJ7hdriqOQUg6Y1w/RTp95ZPPkgbvBW2GsfzUMc=",
            "email": f"testuser{i}@example.com",
            "nickname": f"Tester{i}",
            "realname": f"TestName{i}",
            "age": (i % 60) + 18,
            "first_name": f"FirstName{i}",
            "last_name": f"LastName{i}",
            "gender": "M" if i % 2 == 0 else "W",
            "birth_date": f"19{80 + (i % 20)}-{(i % 12) + 1:02}-{(i % 28) + 1:02}",
            "house_bank": f"Bank{(i % 5) + 1}"
        }
    })

with open("custom_users.json", "w") as f:
    json.dump(data, f, indent=4)

print("custom_users.json 생성 완료")