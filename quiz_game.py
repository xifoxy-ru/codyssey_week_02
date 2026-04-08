from quiz import Quiz

class QuizGame:
    """콘솔 기반 퀴즈 게임의 메뉴 흐름을 관리하는 클래스."""

    def __init__(self):
        """기본 게임 상태를 초기화한다."""
        self.is_running = True

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
        """퀴즈 풀기 메뉴의 임시 동작."""
        print("퀴즈 풀기 기능은 아직 구현 전입니다.")

    def add_quiz(self):
        """퀴즈 추가 메뉴의 임시 동작."""
        print("퀴즈 추가 기능은 아직 구현 전입니다.")

    def show_quiz_list(self):
        """퀴즈 목록 메뉴의 임시 동작."""
        print("퀴즈 목록 기능은 아직 구현 전입니다.")

    def show_score(self):
        """점수 확인 메뉴의 임시 동작."""
        print("점수 확인 기능은 아직 구현 전입니다.")

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
