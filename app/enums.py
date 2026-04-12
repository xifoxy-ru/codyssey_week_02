from enum import IntEnum


class MenuOption(IntEnum):
    """메뉴 선택 번호를 정의한다."""

    PLAY_QUIZ = 1
    ADD_QUIZ = 2
    SHOW_QUIZ_LIST = 3
    SHOW_SCORE = 4
    DELETE_QUIZ = 5
    EXIT = 6