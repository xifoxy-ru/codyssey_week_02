class FileConfig:
    """파일 및 시스템 관련 상수를 정의한다."""

    DEFAULT_QUIZ_FILE = "data/default_quizzes.json"
    STATE_FILE = "data/state.json"
    ENCODING = "utf-8"
    JSON_INDENT = 2
    CLEAR_COMMAND_WINDOWS = "cls"
    CLEAR_COMMAND_POSIX = "clear"


class GameRule:
    """게임 규칙 관련 상수를 정의한다."""

    MENU_MIN = 1
    MENU_MAX = 6
    CHOICE_MIN = 1
    CHOICE_COUNT = 4
    INITIAL_BEST_SCORE = 0
    MIN_SCORE = 0
    HINT_PENALTY = 5
    HISTORY_PREVIEW_LIMIT = 5
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class JsonKey:
    """JSON 저장 구조에서 사용하는 키를 정의한다."""

    QUIZZES = "quizzes"
    QUESTION = "question"
    CHOICES = "choices"
    ANSWER = "answer"
    HINT = "hint"
    BEST_SCORE = "best_score"
    SCORE_HISTORY = "score_history"
    PLAYED_AT = "played_at"
    QUESTION_COUNT = "question_count"
    CORRECT_COUNT = "correct_count"
    HINT_USED_COUNT = "hint_used_count"
    SCORE = "score"


class InputValue:
    """입력 해석에 사용하는 상수를 정의한다."""

    YES_VALUES = ("y", "yes")
    NO_VALUES = ("n", "no")


class Text:
    """화면 출력 문구와 템플릿을 정의한다."""

    APP_TITLE = "=== 나만의 퀴즈 게임 ==="

    MENU_PLAY_QUIZ = "1. 퀴즈 풀기"
    MENU_ADD_QUIZ = "2. 퀴즈 추가"
    MENU_SHOW_QUIZ_LIST = "3. 퀴즈 목록"
    MENU_SHOW_SCORE = "4. 점수 확인"
    MENU_DELETE_QUIZ = "5. 퀴즈 삭제"
    MENU_EXIT = "6. 종료"

    SECTION_PLAY_QUIZ = "=== 퀴즈 풀기 ==="
    SECTION_QUIZ_RESULT = "=== 퀴즈 결과 ==="
    SECTION_ADD_QUIZ = "=== 퀴즈 추가 ==="
    SECTION_QUIZ_LIST = "=== 퀴즈 목록 ==="
    SECTION_SHOW_SCORE = "=== 점수 확인 ==="
    SECTION_DELETE_QUIZ = "=== 퀴즈 삭제 ==="

    PAUSE_PROMPT = "\n엔터를 누르면 메뉴로 돌아갑니다...\n"
    
    MENU_PROMPT = "메뉴 번호를 입력하세요: "
    ANSWER_PROMPT = "정답 번호를 입력하세요: "
    QUIZ_COUNT_PROMPT = "몇 문제를 풀겠습니까?: "
    QUIZ_DELETE_PROMPT = "삭제할 퀴즈 번호를 입력하세요: "
    QUESTION_PROMPT = "문제를 입력하세요: "
    CHOICE_PROMPT_TEMPLATE = "{index}번 선택지를 입력하세요: "
    ANSWER_NUMBER_PROMPT = "정답 번호를 입력하세요 (1~4): "
    HINT_INPUT_PROMPT = "힌트를 입력하세요 (선택): "
    CONFIRM_DELETE_PROMPT = "정말 삭제하시겠습니까? (y/n): "

    FILE_NOT_FOUND_TEMPLATE = "{file_path} 파일이 없어 기본값으로 진행합니다."
    FILE_BROKEN_TEMPLATE = "{file_path} 파일이 손상되어 기본값으로 진행합니다."
    FILE_READ_ERROR_TEMPLATE = "{file_path} 파일을 읽는 중 오류가 발생했습니다."

    DEFAULT_QUIZ_TYPE_ERROR = "기본 퀴즈 데이터 형식이 올바르지 않아 빈 목록으로 처리합니다."
    INVALID_QUIZ_ITEM = "잘못된 퀴즈 데이터 항목을 건너뜁니다."
    INVALID_QUESTION = "문제 형식이 올바르지 않은 항목을 건너뜁니다."
    INVALID_CHOICES = "선택지 형식이 올바르지 않은 항목을 건너뜁니다."
    INVALID_CHOICE_CONTENT = "선택지 내용이 올바르지 않은 항목을 건너뜁니다."
    INVALID_ANSWER = "정답 번호가 올바르지 않은 항목을 건너뜁니다."
    EMPTY_DEFAULT_QUIZZES = "기본 퀴즈 데이터도 비어 있어 빈 상태로 시작합니다."
    STATE_SAVE_ERROR = "state.json 저장 중 오류가 발생했습니다."
    STATE_QUIZZES_TYPE_ERROR = "state.json의 quizzes 형식이 올바르지 않아 복구를 시도합니다."
    STATE_BEST_SCORE_TYPE_ERROR = "state.json의 best_score 형식이 올바르지 않아 0으로 초기화합니다."
    STATE_HISTORY_TYPE_ERROR = "state.json의 score_history 형식이 올바르지 않아 빈 목록으로 초기화합니다."
    STATE_INVALID_QUIZ_DATA = "state.json의 퀴즈 데이터가 잘못되어 기본 퀴즈로 복구합니다."

    EMPTY_MENU_INPUT = "입력이 비어 있습니다. 1부터 6까지 입력하세요."
    EMPTY_ANSWER_INPUT = "입력이 비어 있습니다. 정답 번호를 입력하세요."
    EMPTY_NUMBER_INPUT = "입력이 비어 있습니다. 숫자를 입력하세요."
    EMPTY_TEXT_INPUT = "빈 값은 입력할 수 없습니다."
    NUMBER_ONLY = "숫자만 입력할 수 있습니다."
    MENU_RANGE_ERROR = "메뉴 번호는 1부터 6까지 입력해야 합니다."
    ANSWER_RANGE_TEMPLATE = "정답 번호는 1부터 {max_value}까지 입력해야 합니다."
    NUMBER_RANGE_TEMPLATE = "{min_value}부터 {max_value}까지의 숫자를 입력하세요."
    YES_NO_ONLY = "y 또는 n만 입력할 수 있습니다."

    INTERRUPT_MENU = "\n입력이 중단되었습니다. 다시 메뉴로 돌아갑니다."
    INTERRUPT_RETRY = "\n입력이 중단되었습니다. 다시 입력을 받습니다."
    INTERRUPT_ANSWER = "\n입력이 중단되었습니다. 다시 문제 입력을 받습니다."
    INTERRUPT_HINT_SKIP = "\n입력이 중단되었습니다. 힌트 없이 진행합니다."
    INTERRUPT_DELETE_CANCEL = "\n입력이 중단되었습니다. 삭제를 취소합니다."
    EOF_SAFE_EXIT = "\n입력이 종료되어 프로그램을 종료합니다."

    NO_REGISTERED_QUIZ = "등록된 퀴즈가 없습니다."
    NO_QUIZ_TO_DELETE = "삭제할 퀴즈가 없습니다."
    NO_SCORE_HISTORY = "저장된 점수 기록이 없습니다."

    TOTAL_QUIZ_COUNT_TEMPLATE = "현재 풀 수 있는 문제는 총 {max_count}개입니다."
    PROGRESS_TEMPLATE = "\n[{index}/{total_count}]"
    CORRECT = "정답입니다."
    WRONG = "오답입니다."
    CORRECT_ANSWER_TEMPLATE = "정답은 {answer}번: {correct_text}"
    BEST_SCORE_UPDATED = "최고 점수가 갱신되었습니다."

    RESULT_CORRECT_COUNT_TEMPLATE = "정답 수: {correct_count}/{total_count}"
    RESULT_HINT_USED_TEMPLATE = "힌트 사용 횟수: {hint_used_count}회"
    RESULT_SCORE_TEMPLATE = "점수: {score}점"
    RESULT_BEST_SCORE_TEMPLATE = "최고 점수: {best_score}점"

    QUIZ_ADDED = "새 퀴즈가 추가되었습니다."
    QUIZ_COUNT_TEMPLATE = "현재 등록된 퀴즈 수: {quiz_count}개"

    SELECTED_QUIZ_TEMPLATE = "\n선택한 퀴즈: {question}"
    DELETE_CANCELLED = "퀴즈 삭제를 취소했습니다."
    QUIZ_DELETED = "퀴즈가 삭제되었습니다."
    DELETED_QUESTION_TEMPLATE = "삭제된 문제: {question}"

    HINT_TEMPLATE = "힌트: {hint}"
    HINT_GUIDE = "\n[힌트: 힌트를 보려면 Y를 입력해주세요.]"
    NO_HINT = "이 문제에는 힌트가 없습니다."
    HINT_ALREADY_SHOWN = "이미 힌트를 확인했습니다."
    ANSWER_OR_Y_ONLY = "숫자 또는 Y만 입력할 수 있습니다."
    HINT_PENALTY_TEMPLATE = "힌트를 사용하면 {penalty}점 차감됩니다."

    RECENT_SCORE_HISTORY = "\n최근 점수 기록:"
    SCORE_HISTORY_TEMPLATE = (
        "{index}. {played_at} | "
        "문제 수: {question_count} | "
        "정답 수: {correct_count} | "
        "힌트 사용: {hint_used_count} | "
        "점수: {score}점"
    )

    EXIT_MESSAGE = "프로그램을 종료합니다."