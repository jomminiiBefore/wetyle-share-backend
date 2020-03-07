## Wetyle Share 프로젝트 소개_Back-End
10~20대 여성을 주요 고객으로 가진 SNS & 커머스 서비스인 [스타일쉐어](https://www.styleshare.kr/) 클론 프로젝트
- [github 확인하기](https://github.com/wecode-bootcamp-korea/wetyle-share-backend)

### 개발 인원 및 기간
- 개발기간 : 2020/2/23 ~ 2020/3/6
- 개발 인원 : 프론트엔트 4명, 백엔드 2명
- [프론트엔드 github](https://github.com/wecode-bootcamp-korea/wetyle-share-frontend)

### 목적
주변 개발자분들에게서 SNS와 커머스 서비스를 경험하면 백엔드가 지녀야할 역량을 많은 부분 갖출 수 있다고 들었고, 이 두 가지 요소를 모두 담고 있는 스타일쉐어를 분석하고 주요 기능을 클론함으로써 이를 이루고자 함

### 데모 영상(이미지 클릭)

[![위스타일 데모 영상](https://images.velog.io/images/devmin/post/48a64649-611c-4ee9-9b81-880eaa7914d8/%E1%84%89%E1%85%B3%E1%84%89%E1%85%A3%E1%86%BA%2015.png)](https://www.youtube.com/watch?v=Wd_x8jr5elM)

<br>

## 적용 기술 및 구현 기능
### 적용 기술
- Python, Django web framework
- Beautifulsoup, Selenium
- Bcrypt
- JWT
- KAKAO social login
- AWS EC2, RDS, S3
- CORS headers

</br>


### 구현 기능
#### 공통
- Beautifulsoup, Selenium을 이용한 웹 크롤링
- Bcrypt를 활용한 비밀번호 암호화
- JWT를 활용한 로그인 토큰 발행
- 일반 회원가입 / 로그인
- 카카오 소셜 로그인
- 이메일 유효성 검사
- AWS EC2에 서버 배포
- AWS RDS에 DB 세팅 및 EC2 서버 연결
- AWS S3에 업로드 이미지 저장, UUID를 이용한 URL 난수값 생성

</br>

#### OOTD(SNS 섹션)
- 카드 리스트 반환
	- 최신 : 작성 순
	- 인기 : 팔로워 수/ 좋아요 수 순
	- 팔로잉 : 팔로잉한 사람들이 올린 게시물 최신 순
- 스타일 카드 내부 페이지 반환
- 유저간 팔로우 / 언팔로우
- 게시물 좋아요 / 안좋아요
- 컬렉션에 스타일 담기(게시물 간 관계 설정)
- 게시물, 댓글 업로드
- 업로드 이미지 AWS s3 저장 및 url 발급

</br>


#### STORE(커머스 섹션)
- 상품 좋아요 / 안좋아요
- 상품 리스트 반환
	- 인기 상품 : 상품 좋아요 순
	- 인기 키워드 : 해당 키워드 검색 결과
	- 인기 브랜드 : 브랜드 별 상품 보유 순
- 상품 상세페이지 데이터 반환

</br>

### API 문서(with POSTMAN)
- [백엔드 API 확인하기](https://documenter.getpostman.com/view/10398706/SzRw2B3K?version=latest)

</br>

### 데이터 모델링 ERD(with AQueryTool)
![데이터 모델링](https://images.velog.io/images/devmin/post/3f3c0567-24ef-44cd-8f79-8ba9368998c1/wetyle-share-ERD.png)

- 상품후기, Q&A, 장바구니, 기획전 부분은 모델링만하고 시간상 구현 제외



