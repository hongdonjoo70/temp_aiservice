# AI 챗봇 컨테이너 모음

이 저장소는 Flask 기반 한국어 챗봇 예제와 기능별 변형을 담고 있습니다. 각 컨테이너는 독립적으로 실행할 수 있도록 앱, 프롬프트, API 연동 코드를 폴더별로 관리합니다.

## 구성

- `toolcontainer/`: 함수 호출형 챗봇. 날씨, 환율, 웹 검색 도구를 제공합니다.
- `container/`, `FirstContainer/`: 기본 챗봇 예제.
- `AgentContainer/`: 에이전트 기반 확장.
- `DBContainer/`: 데이터베이스 및 메모리 기능을 포함한 확장.
- `VectorContainer/`: 벡터 검색과 대화 메모리 기능을 포함한 확장.
- `systemrole_func/`: 시스템 프롬프트 및 함수 호출 관련 코드.
- `test/`: 데이터베이스, 임베딩 연결 확인용 스크립트.

## `toolcontainer` 실행

Python 가상 환경에서 필요한 패키지를 설치합니다.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install Flask openai python-dotenv tiktoken pytz requests tavily-python
```

macOS 또는 Linux:

```bash
source .venv/bin/activate
python -m pip install Flask openai python-dotenv tiktoken pytz requests tavily-python
```

저장소 루트에 `.env` 파일을 만들고 API 키를 설정합니다.

```dotenv
HASA_API_KEY=발급받은_HASA_API_키
TAVILY_API_KEY=발급받은_Tavily_API_키
```

`HASA_API_KEY`는 OpenAI 호환 Hasa API 클라이언트 인증에 사용되고, `TAVILY_API_KEY`는 웹 검색 도구에 사용됩니다. 키가 없으면 API 호출 또는 웹 검색이 실패합니다. 실제 키를 저장소에 커밋하지 마세요.

앱을 실행합니다.

```bash
python toolcontainer/app.py
```

브라우저에서 `http://localhost:8080/chat-app`을 열어 채팅할 수 있습니다. `POST /chat-api`는 `{ "request_message": "질문" }` JSON을 받고 `{ "response_message": "답변" }`을 반환합니다. 루트 경로 `/`는 간단한 상태 문자열을 반환합니다.

## 공통 모듈

`toolcontainer/common.py`는 환경 변수 로드, 모델 이름 모음, OpenAI 호환 API 클라이언트, 토큰 수 추정, 한국 시간 날짜 및 시각 함수를 제공합니다.

- `model`: 모델 식별자를 보관하는 변경 불가 데이터 클래스 인스턴스입니다. `toolcontainer/app.py`에서는 `model.gpt_oss_120b`를 사용합니다.
- `client`: `https://open.hasa.re.kr/v1`을 기본 주소로 사용하는 OpenAI 클라이언트입니다. 인증 키는 `HASA_API_KEY`에서 읽습니다.
- `gpt_num_tokens(messages, model=...)`: 메시지 내용을 토큰화해 입력 크기를 대략 계산합니다. 모델 인코딩을 찾지 못하면 `cl100k_base`를 사용합니다.
- `makeup_response(message, finish_reason=...)`: API 응답과 유사한 딕셔너리 형태의 오류 응답을 만듭니다.
- `today()`, `yesterday()`: 한국 시간 기준 날짜를 `YYYYMMDD`로 반환합니다.
- `currTime()`: 한국 시간 기준 시각을 `YYYY.MM.DD HH:MM:SS`로 반환합니다.

모듈 내 클라이언트는 가져오는 시점에 생성됩니다. 다른 컨테이너에서 공통 코드를 사용할 때는 해당 컨테이너를 실행 경로에 두어 `common` 모듈을 올바르게 불러오세요.

## 참고

현재 저장소에는 통합 의존성 목록 파일이 없습니다. 컨테이너별 확장 기능은 추가 라이브러리나 API 키를 요구할 수 있으므로, 각 폴더의 코드와 `.env.example`을 확인한 뒤 실행 환경을 구성하세요.
