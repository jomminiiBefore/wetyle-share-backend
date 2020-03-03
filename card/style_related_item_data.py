import random

pants = ['nike', 'adidas', 'newbalance', 'puma', 'gucci', 'made by wecode', '없음' ]
skirt = ['키싱유 체크플리츠 미니스커트', '캉캉 미니스커트','방울방울도트 스커트', '자베르 코튼 롱스커트', '없음']
shoes = ['스니커즈', '운동화', '부츠', '장화', '슬리퍼', '맨발','없음']
bag   = ['힙백', '배낭', '신발주머니', '에코백', '없음']
accessory = ['스와로브스키 귀걸이', '청동 목걸이', '다이아몬드 반지', '없음']
etc = ['없음', '이게 뭔가 싶다', '주먹도끼', '청동거울']

def random_item():
    related_items = {
        "pants"     : pants[random.randint(0,len(pants)-1)],
        "skirt"     : skirt[random.randint(0,len(skirt)-1)],
        "shoes"     : shoes[random.randint(0,len(shoes)-1)],
        "bag"       : bag[random.randint(0,len(bag)-1)],
        "accessory" : accessory[random.randint(0,len(accessory)-1)],
        "etc"       : etc[random.randint(0,len(etc)-1)]
        }
    return related_items
