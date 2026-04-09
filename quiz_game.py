import json
import os

from quiz import Quiz


class QuizGame:
    """콘솔 기반 퀴즈 게임의 메뉴 흐름을 관리하는 클래스."""

    def __init__(self):
        """기본 게임 상태를 초기화한다."""
        self.is_running = True
        self.default_quiz_file = "default_quizzes.json"
        self.state_file = "state.json"
        self.quizzes = self.load_quizzes()
        self.best_score = 0

    def load_default_quiz_data(self):
        """기본 퀴즈 데이터 파일을 읽어 리스트로 반환한다.

        Returns:
            list[dict]: 기본 퀴즈 데이터 목록
        """
        with open(self.default_quiz_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def create_quiz_objects(self, quiz_data_list):
        """딕셔너리 목록을 Quiz 객체 목록으로 변환한다.

        Args:
            quiz_data_list (list[dict]): 퀴즈 데이터 목록

        Returns:
            list[Quiz]: Quiz 객체 목록
        """
        quizzes = []

        for quiz_data in quiz_data_list:
            quiz = Quiz(
                question=quiz_data["question"],
                choices=quiz_data["choices"],
                answer=quiz_data["answer"],
                hint=quiz_data.get("hint", ""),
            )
            quizzes.append(quiz)

        return quizzes

    def save_state(self):
        """현재 퀴즈 목록을 state.json 파일에 저장한다."""
        state_data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
        }

        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(state_data, file, ensure_ascii=False, indent=2)

    def load_quizzes(self):
        """state.json 또는 기본 퀴즈 파일에서 퀴즈를 불러온다.

        Returns:
            list[Quiz]: Quiz 객체 목록
        """
        if os.path.exists(self.state_file):
            with open(self.state_file, "r", encoding="utf-8") as file:
                state_data = json.load(file)

            quiz_data_list = state_data.get("quizzes", [])
            return self.create_quiz_objects(quiz_data_list)

        quiz_data_list = self.load_default_quiz_data()
        quizzes = self.create_quiz_objects(quiz_data_list)
        self.quizzes = quizzes
        self.save_state()
        return quizzes

    def display_menu(self):
        """메인 메뉴를 출력한다."""
        print("\n=== 나만의 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")

    def get_menu_choice(self):
        """사용자에게 메뉴 번호를 입력받고 검증한다.

        Returns:
            int: 1~6 사이의 유효한 메뉴 번호
        """
        while True:
            try:
                raw_value = input("메뉴 번호를 입력하세요: ").strip()

                if not raw_value:
                    print("입력이 비어 있습니다. 1부터 6까지 입력하세요.")
                    continue

                choice = int(raw_value)

                if 1 <= choice <= 6:
                    return choice

                print("메뉴 번호는 1부터 6까지 입력해야 합니다.")

            except ValueError:
                print("숫자만 입력할 수 있습니다.")
            except KeyboardInterrupt:
                print("\n입력이 중단되었습니다. 다시 메뉴로 돌아갑니다.")
            except EOFError:
                print("\n입력이 종료되어 프로그램을 종료합니다.")
                self.is_running = False
                return 6

    def get_answer_choice(self, quiz):
        """문제의 정답 번호를 입력받고 검증한다.

        Args:
            quiz (Quiz): 현재 출제 중인 퀴즈 객체

        Returns:
            int: 유효한 정답 번호
        """
        choice_count = len(quiz.choices)

        while True:
            try:
                raw_value = input("정답 번호를 입력하세요: ").strip()

                if not raw_value:
                    print("입력이 비어 있습니다. 정답 번호를 입력하세요.")
                    continue

                answer = int(raw_value)

                if 1 <= answer <= choice_count:
                    return answer

                print(f"정답 번호는 1부터 {choice_count}까지 입력해야 합니다.")

            except ValueError:
                print("숫자만 입력할 수 있습니다.")
            except KeyboardInterrupt:
                print("\n입력이 중단되었습니다. 다시 문제 입력을 받습니다.")
            except EOFError:
                print("\n입력이 종료되어 프로그램을 종료합니다.")
                self.is_running = False
                return choice_count

    def get_non_empty_input(self, prompt):
        """비어 있지 않은 문자열 입력을 받는다.

        Args:
            prompt (str): 입력 안내 문구

        Returns:
            str: 공백이 제거된 입력 문자열
        """
        while True:
            try:
                value = input(prompt).strip()

                if value:
                    return value

                print("빈 값은 입력할 수 없습니다.")

            except KeyboardInterrupt:
                print("\n입력이 중단되었습니다. 다시 입력을 받습니다.")
            except EOFError:
                print("\n입력이 종료되어 프로그램을 종료합니다.")
                self.is_running = False
                return ""

    def get_optional_input(self, prompt):
        """선택 입력 문자열을 받는다.

        Args:
            prompt (str): 입력 안내 문구

        Returns:
            str: 공백이 제거된 입력 문자열
        """
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print("\n입력이 중단되었습니다. 힌트 없이 진행합니다.")
            return ""
        except EOFError:
            print("\n입력이 종료되어 프로그램을 종료합니다.")
            self.is_running = False
            return ""

    def get_choice_number_input(self, prompt, min_value, max_value):
        """지정된 범위의 숫자 입력을 받는다.

        Args:
            prompt (str): 입력 안내 문구
            min_value (int): 최소값
            max_value (int): 최대값

        Returns:
            int: 검증된 숫자 입력값
        """
        while True:
            try:
                raw_value = input(prompt).strip()

                if not raw_value:
                    print("입력이 비어 있습니다. 숫자를 입력하세요.")
                    continue

                number = int(raw_value)

                if min_value <= number <= max_value:
                    return number

                print(f"{min_value}부터 {max_value}까지의 숫자를 입력하세요.")

            except ValueError:
                print("숫자만 입력할 수 있습니다.")
            except KeyboardInterrupt:
                print("\n입력이 중단되었습니다. 다시 입력을 받습니다.")
            except EOFError:
                print("\n입력이 종료되어 프로그램을 종료합니다.")
                self.is_running = False
                return max_value

    def update_best_score(self, score):
        """현재 점수와 최고 점수를 비교해 갱신한다.

        Args:
            score (int): 이번 플레이 점수
        """
        if score > self.best_score:
            self.best_score = score
            print("최고 점수가 갱신되었습니다.")

    def handle_menu(self, choice):
        """선택한 메뉴 번호에 따라 동작한다.

        Args:
            choice (int): 사용자가 선택한 메뉴 번호
        """
        if choice == 1:
            self.play_quiz()
        elif choice == 2:
            self.add_quiz()
        elif choice == 3:
            self.show_quiz_list()
        elif choice == 4:
            self.show_score()
        elif choice == 5:
            self.delete_quiz()
        elif choice == 6:
            self.exit_game()

    def play_quiz(self):
        """등록된 퀴즈를 순서대로 출제하고 결과를 출력한다."""
        print("\n=== 퀴즈 풀기 ===")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0
        total_count = len(self.quizzes)

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{index}/{total_count}]")
            quiz.display()

            user_answer = self.get_answer_choice(quiz)

            if not self.is_running:
                return

            if quiz.is_correct(user_answer):
                correct_count += 1
                print("정답입니다.")
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print("오답입니다.")
                print(f"정답은 {quiz.answer}번: {correct_text}")

        score = int((correct_count / total_count) * 100)
        self.update_best_score(score)

        print("\n=== 퀴즈 결과 ===")
        print(f"정답 수: {correct_count}/{total_count}")
        print(f"점수: {score}점")
        print(f"최고 점수: {self.best_score}점")

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가한다."""
        print("\n=== 퀴즈 추가 ===")

        question = self.get_non_empty_input("문제를 입력하세요: ")

        if not self.is_running:
            return

        choices = []

        for index in range(1, 5):
            choice = self.get_non_empty_input(f"{index}번 선택지를 입력하세요: ")

            if not self.is_running:
                return

            choices.append(choice)

        answer = self.get_choice_number_input("정답 번호를 입력하세요 (1~4): ", 1, 4)

        if not self.is_running:
            return

        hint = self.get_optional_input("힌트를 입력하세요 (선택): ")

        if not self.is_running:
            return

        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
        self.quizzes.append(new_quiz)
        self.save_state()

        print("새 퀴즈가 추가되었습니다.")
        print(f"현재 등록된 퀴즈 수: {len(self.quizzes)}개")

    def show_quiz_list(self):
        """등록된 퀴즈 목록을 출력한다."""
        print("\n=== 퀴즈 목록 ===")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    def show_score(self):
        """현재 최고 점수를 출력한다."""
        print("\n=== 점수 확인 ===")
        print(f"현재 최고 점수: {self.best_score}점")

    def delete_quiz(self):
        """퀴즈 삭제 메뉴의 임시 동작."""
        print("퀴즈 삭제 기능은 아직 구현 전입니다.")

    def exit_game(self):
        """프로그램을 종료한다."""
        print("프로그램을 종료합니다.")
        self.is_running = False

    def run(self):
        """게임 메인 루프를 실행한다."""
        while self.is_running:
            self.display_menu()
            choice = self.get_menu_choice()

            if not self.is_running:
                break

            self.handle_menu(choice)