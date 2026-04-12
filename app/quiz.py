class Quiz:
    """퀴즈 1개를 표현하는 클래스."""

    def __init__(self, question, choices, answer, hint=""):
        """Quiz 객체를 초기화한다.

        Args:
            question (str): 문제 내용
            choices (list[str]): 선택지 목록
            answer (int): 정답 번호 (1부터 시작)
            hint (str, optional): 힌트 내용. 기본값은 빈 문자열
        """
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self):
        """문제와 선택지를 출력한다."""
        print(f"\n문제: {self.question}")

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """사용자 입력이 정답인지 확인한다.

        Args:
            user_answer (int): 사용자가 입력한 답

        Returns:
            bool: 정답이면 True, 아니면 False
        """
        return user_answer == self.answer

    def to_dict(self):
        """Quiz 객체를 딕셔너리로 변환한다.

        Returns:
            dict: JSON 저장용 딕셔너리
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }
