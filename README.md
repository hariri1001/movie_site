
### 1. 프로젝트 소개
   - 개발 기간
   11/18 ~ 26

   - 프로젝트 내용
   영화 추천 서비스

   - 기술 스택
   Django, Vue, Html, CSS, Python, Bootstrap, Figma

   - 개발 인원
   2명 (최재혁, 이하리)

### 2. 주요 기능
   - 회원가입
   - 로그인 및 로그아웃
   - 프로필
   - 좋아요 (영화)
   - 프로필 조회 (상대방 유저)
   - 팔로우 (유저)
   - 영화 목록 조회(메인 페이지)
   - 영화 상세 조회
   - 영화 검색 기능
   - 커뮤니티 게시글 기능
   - 커뮤니티 댓글 기능
   - 영화 추천 알고리즘(챗봇)
   - 영화 추천 서비스 (카드 선택)
   - 사용자 선호도 기반 챗봇 기능

   - 피그마 작업
   - 발표 준비 (ppt, 대본)
   - 메인 화면에 최근 게시글

### 3. 서비스 설계
   - 와이어프레임 -> 피그마
   - 데이터 베이스 모델링 (ERD)
   - URL 명세서(or REST API 명세)
   - Vue 컴포넌트 구조


   - 팀원 및 업무분담

    최재혁
    - ERD
    - 페이지 레이아웃 설계
    - 아이디어 기획
    - 피그마 디자인
    - 디자인 수정
    - 레퍼런스 수집
    - 발표 


    이하리
    - 프로젝트 일정 조율
    - 페이지 레이아웃 설계
    - ERD
    - 로그인/로그아웃/회원가입 기능구현(BE&FE)
    - 프로필 기능구현(BE&FE)
    - 팔로우/팔로잉 기능구현(BE&FE)
    - 영화 목록/상세/검색 기능구현(BE&FE)
    - 게시글 생성/수정/삭제 기능구현(BE&FE)
    - 추천 서비스 (카드셔플) 기능구현(BE&FE)
    - 챗봇 기능 기능구현(BE&FE)
    

### 4. ERD
![My Image](/erd.png)


### 5. API 입력 위치
 - 변수명 API_KEY에 할당
 - API키를 .env에서 찾아서 입력


### 6. 추천 알고리즘에 대한 기술적 설명
   영화 추천 챗봇:

   사용자에게 선호하는 영화 장르, 중요하게 생각하는 요소, 선호하는 영화 분위기 등의 질문을 던지고 그에 대한 답변을 수집합니다.
   사용자의 답변을 기반으로 Django 백엔드 서버의 /movies/api/recommend/ API에 POST 요청을 보내 영화 추천을 받아옵니다.
   받아온 추천 영화 목록을 TMDB API를 이용해 영화 포스터, 설명, 개봉일, 평점, 상영시간, 장르, 원제 등의 상세 정보를 가져와 보완합니다.
   추천된 영화 정보를 화면에 카드 형식으로 보여주며, 영화 정보가 로딩 중이거나 에러가 발생한 경우 적절한 메시지를 표시합니다.
   사용자가 '다시 시작하기' 버튼을 누르면 추천 결과와 답변 내역을 초기화하고 처음부터 다시 시작할 수 있습니다.


   랜덤 영화 추천(카드 셔플):

   TMDB API의 discover/movie 엔드포인트를 이용해 인기 있는 영화 중 랜덤으로 5개의 영화를 가져옵니다.
   가져온 영화 정보를 바탕으로 5장의 타로카드 형태의 UI를 구성합니다.
   사용자가 카드를 클릭하면 해당 카드가 뒤집히며, 뒷면에는 영화 포스터와 제목이 표시됩니다.
   뒤집힌 카드를 한번 더 클릭하면 해당 영화의 상세 정보를 보여주는 모달 창이 나타납니다.
   '다시 뽑기' 버튼을 누르면 현재 표시된 카드를 초기화하고 새로운 5개의 랜덤 영화를 다시 가져와 표시합니다.
   카드 애니메이션과 반짝이는 효과를 통해 시각적인 즐거움을 더했습니다.



   두 컴포넌트 모두 TMDB API를 활용하여 영화 정보를 가져오는 것이 특징입니다.
   MovieRecommender는 사용자의 취향을 입력받아 맞춤형 영화를 추천해주는 반면, 랜덤 영화 추천 컴포넌트는 인기 있는 영화 중 무작위로 선택하여 사용자에게 새로운 영화를 발견할 기회를 제공합니다.
   시각적으로는 MovieRecommender가 설문 형식의 UI와 추천 결과 카드로 구성된 반면, 랜덤 영화 추천은 타로카드를 모티브로 한 신비롭고 인터랙티브한 UI를 제공하여 사용자의 흥미를 유발하는 것이 특징입니다.




### 7. 후기
   - 팀장(최재혁):
   이번 프로젝트에서 ERD 설계, 페이지 레이아웃 설계, 아이디어 기획, 피그마 디자인, 디자인 수정, 레퍼런스 수집, 발표까지 다양한 역할을 맡으며 프로젝트의 전반적인 흐름을 깊이 이해할 수 있었습니다. ERD 설계를 통해 데이터를 구조화하고 명확히 정의하면서 데이터베이스 구성의 중요성을 깨달았고, 페이지 레이아웃 설계에서는 사용자 경험을 최우선으로 고려하여 직관적이고 효율적인 화면 구성을 고민했습니다. 아이디어 기획 단계에서는 팀원들과의 협업을 통해 다양한 관점을 공유하며 사용자가 실질적인 가치를 느낄 수 있는 기능을 구상할 수 있었고, 피그마 디자인과 수정 작업에서는 시각적인 완성도를 높이는 동시에 디자인이 개발 과정에서의 구현 가능성과도 잘 연결되도록 신경 썼습니다. 또한, 레퍼런스 수집을 통해 기존 사례를 분석하며 프로젝트의 차별화를 고민했고, 마지막으로 발표를 준비하며 프로젝트의 핵심 가치를 명확히 전달하기 위해 노력했습니다. 이번 경험을 통해 기획, 디자인, 개발의 전 과정을 아우르는 포괄적인 시각을 키울 수 있었고, 역할마다 겪은 고민과 도전이 모두 성장의 밑거름이 되었음을 느낍니다.

   - 팀원(이하리):
   9일간의 짧은 기간 동안 풀스택 영화 추천 서비스를 구현하면서 많은 것을 배우고 성장할 수 있었습니다. Django와 Vue.js를 활용한 실제 서비스 개발 경험을 통해 프론트엔드와 백엔드 간의 유기적인 연결의 중요성을 체감했습니다. 특히 두 프레임워크를 동시에 다루면서 각각의 특성과 장점을 이해할 수 있었고, RESTful API 설계 및 구현을 통해 실제 서비스 아키텍처를 경험할 수 있었습니다. Vue.js의 컴포넌트 기반 개발과 상태 관리, RESTful API 설계 원칙을 적용하면서 웹 개발의 전체적인 흐름을 이해할 수 있었고, 한정된 시간 내에서 기능 우선순위를 설정하고 시간을 관리하는 법도 배웠습니다.
다만 짧은 개발 기간으로 인해 코드의 재사용성과 유지보수성을 충분히 고려하지 못한 점이 아쉬움으로 남습니다. 특히 사용자 경험(UX)을 더욱 개선하고, 영화 추천 알고리즘을 더 정교화하며, 테스트 코드 작성을 통한 안정성 확보가 부족했다고 느꼈습니다. 또한 기능 구현에 집중하다 보니 성능 최적화나 보안 측면에서의 고려가 부족했던 점도 아쉬운 부분입니다.
하지만 이번 프로젝트를 통해 실제 서비스 개발에 필요한 다양한 기술과 프로세스를 경험할 수 있었습니다. 이러한 경험과 아쉬웠던 점들을 교훈 삼아 다음 프로젝트시에는 더 나은 결과를 위해 노력할것입니다.
