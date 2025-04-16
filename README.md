# LBRX
https://srv.lbrx.net

## lbrxAuth
models.py:

    User: Django의 AbstractUser를 확장하여 게임 관련 필드 (예: 마지막 접속 시간, 현재 위치 등) 추가
    World: 게임 세계 정보 (맵 정보 연결 등)
    Location: 게임 내 위치 정보 (좌표, 지역 이름, 연결된 다른 위치 정보 등)

views.py:

    기본적인 상태 확인 API (예: 서버 상태, 접속자 수 등)

urls.py:

    기본 API 엔드포인트 연결
admin 앱: 게임 관리자 기능 (별도의 Django 앱으로 분리하거나, 각 앱의 admin.py 활용)

## lbrxCore


## lbrxCharacter
models.py:

    Character: 캐릭터 정보 (이름, 레벨, 직업, 능력치, 경험치 등)

serializers.py:

    CharacterSerializer: 캐릭터 정보 JSON 변환

views.py:

    캐릭터 생성, 조회, 수정 API
    현재 캐릭터 정보 API

urls.py:

    /characters/, /characters/{character_id}/ 등 캐릭터 관련 API 엔드포인트

## lbrxItem
models.py:

    ItemTemplate: 아이템 기본 정보 (이름, 설명, 종류, 효과 등)
    Inventory: 캐릭터가 소유한 아이템 정보 (캐릭터-아이템 연결, 수량 등)

serializers.py:

    ItemTemplateSerializer, InventorySerializer

views.py:

    아이템 목록 조회 API
    특정 아이템 정보 조회 API
    인벤토리 조회 API
    아이템 획득/사용 API (액션 처리는 다른 앱에서 담당할 수 있음)

urls.py:

    /items/, /items/{item_id}/, /inventory/ 등 아이템 관련 API 엔드포인트

## lbrxMap
models.py:

    Map: 맵 기본 정보 (이름, 크기 등)
    Location: 맵의 각 위치 정보 (좌표, 속성, 연결된 다른 위치 정보, scenario 앱의 시나리오와 연결될 수 있는 필드 추가)
    예: scenario = models.ForeignKey('scenario.Scenario', null=True, blank=True, on_delete=models.SET_NULL)

serializers.py:

    MapSerializer, LocationSerializer (시나리오 정보 포함 여부 결정)

views.py:

    맵 정보 조회 API
    특정 위치 정보 조회 API (해당 위치에 연결된 시나리오 정보 함께 제공)

urls.py:

    맵 관련 API 엔드포인트

## lbrxNPC
models.py:

    MonsterTemplate: 몬스터 기본 정보 (이름, 능력치, 드랍 아이템 등)
    MonsterInstance: 필드에 존재하는 몬스터 인스턴스 정보 (현재 위치, HP 등)

serializers.py:

    MonsterTemplateSerializer, MonsterInstanceSerializer

views.py:

    몬스터 목록 조회 API
    특정 몬스터 정보 조회 API
    필드 몬스터 정보 API

urls.py:

    /monsters/, /monsters/{monster_id}/, /field_monsters/ 등 몬스터 관련 API 엔드포인트

## lbrxAction
views.py:

    이동 액션 처리 API
    전투 액션 처리 API (공격, 스킬 사용 등)
    아이템 사용 액션 처리 API
    상호작용 액션 처리 API (NPC 대화 등)

serializers.py:

    액션 요청 데이터 검증을 위한 Serializer (예: 이동 요청 시 목적지 정보)

urls.py:

    /actions/move/, /actions/battle/, /actions/item/use/ 등 액션 처리 API 엔드포인트

    이동, 전투, 아이템 사용 등 기본적인 액션 처리
(선택 사항) 시나리오 진행 관련 액션 처리 (예: 특정 NPC와 대화 시작, 선택지 선택 등)

## lbrxScenario
models.py:

    Scenario: 시나리오 기본 정보 (제목, 시작 조건 등)
    Event: 시나리오 내의 각 이벤트 정보 (텍스트 내용, 등장 NPC, 아이템 획득/소실, 분기 조건 등)
    Choice: 이벤트 내의 선택지 정보 (선택지 텍스트, 다음 이벤트 연결 정보)
    ScenarioProgress: 각 캐릭터별 시나리오 진행 상황 (현재 진행 중인 시나리오, 현재 이벤트, 선택한 분기 정보 등)

serializers.py:

    ScenarioSerializer, EventSerializer, ChoiceSerializer, ScenarioProgressSerializer

views.py:

    특정 위치에 연결된 시나리오 시작 API
    현재 진행 중인 시나리오 이벤트 정보 조회 API
    선택지 선택 처리 API (클라이언트의 선택에 따라 다음 이벤트 또는 시나리오 분기 처리)

urls.py:

    /scenarios/{scenario_id}/start/, /scenarios/progress/, /scenarios/choices/{choice_id}/select/ 등 시나리오 관련 API 엔드포인트

## lbrxUtil


# etc
chat 앱 (채팅 기능)

    consumers.py: (Django Channels 사용 시) WebSocket Consumer 정의
    routing.py: (Django Channels 사용 시) WebSocket 라우팅 설정

추가적으로 고려할 수 있는 앱:
    quest 앱: 퀘스트 정보 및 진행 상황 관리
    guild 앱: 길드 시스템 관련 기능
