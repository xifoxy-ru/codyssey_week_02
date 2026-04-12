import json
import os
import random
from datetime import datetime

from constants import FileConfig, GameRule, InputValue, JsonKey, Text
from enums import MenuOption
from quiz import Quiz


class QuizGame:
    """콘솔 기반 퀴즈 게임의 메뉴 흐름을 관리하는 클래스."""

    def __init__(self):
        """기본 게임 상태를 초기화한다."""
        self.is_running = True
        self.default_quiz_file = FileConfig.DEFAULT_QUIZ_FILE
        self.state_file = FileConfig.STATE_FILE
        self.hint_penalty = GameRule.HINT_PENALTY
        self.best_score = GameRule.INITIAL_BEST_SCORE
        self.score_history = []
        self.quizzes = self.load_state()

    def clear_screen(self):
        """운영체제에 맞게 콘솔 화면을 정리한다."""
        command = (
            FileConfig.CLEAR_COMMAND_WINDOWS
            if os.name == "nt"
            else FileConfig.CLEAR_COMMAND_POSIX
        )
        os.system(command)

    def pause(self):
        """사용자가 결과를 읽을 수 있도록 잠시 대기한다."""
        try:
            input(Text.PAUSE_PROMPT)
        except (KeyboardInterrupt, EOFError):
            self.is_running = False

    def load_json_file(self, file_path, default_value):
        """JSON 파일을 읽고 실패 시 기본값을 반환한다."""
        try:
            with open(file_path, "r", encoding=FileConfig.ENCODING) as file:
                return json.load(file)
        except FileNotFoundError:
            print(Text.FILE_NOT_FOUND_TEMPLATE.format(file_path=file_path))
        except json.JSONDecodeError:
            print(Text.FILE_BROKEN_TEMPLATE.format(file_path=file_path))
        except OSError:
            print(Text.FILE_READ_ERROR_TEMPLATE.format(file_path=file_path))

        return default_value

    def load_default_quiz_data(self):
        """기본 퀴즈 데이터 파일을 읽어 리스트로 반환한다."""
        quiz_data_list = self.load_json_file(self.default_quiz_file, [])

        if not isinstance(quiz_data_list, list):
            print(Text.DEFAULT_QUIZ_TYPE_ERROR)
            return []

        return quiz_data_list

    def create_quiz_objects(self, quiz_data_list):
        """딕셔너리 목록을 Quiz 객체 목록으로 변환한다."""
        quizzes = []

        for quiz_data in quiz_data_list:
            if not isinstance(quiz_data, dict):
                print(Text.INVALID_QUIZ_ITEM)
                continue

            question = quiz_data.get(JsonKey.QUESTION)
            choices = quiz_data.get(JsonKey.CHOICES)
            answer = quiz_data.get(JsonKey.ANSWER)
            hint = quiz_data.get(JsonKey.HINT, "")

            if not isinstance(question, str) or not question.strip():
                print(Text.INVALID_QUESTION)
                continue

            if not isinstance(choices, list) or len(choices) != GameRule.CHOICE_COUNT:
                print(Text.INVALID_CHOICES)
                continue

            if not all(isinstance(choice, str) and choice.strip() for choice in choices):
                print(Text.INVALID_CHOICE_CONTENT)
                continue

            if (
                not isinstance(answer, int)
                or not GameRule.CHOICE_MIN <= answer <= GameRule.CHOICE_COUNT
            ):
                print(Text.INVALID_ANSWER)
                continue

            if not isinstance(hint, str):
                hint = ""

            quiz = Quiz(
                question=question.strip(),
                choices=[choice.strip() for choice in choices],
                answer=answer,
                hint=hint.strip(),
            )
            quizzes.append(quiz)

        return quizzes

    def create_initial_state_data(self):
        """초기 state 데이터를 생성한다."""
        quiz_data_list = self.load_default_quiz_data()
        quizzes = self.create_quiz_objects(quiz_data_list)

        if not quizzes:
            print(Text.EMPTY_DEFAULT_QUIZZES)
            return {
                JsonKey.QUIZZES: [],
                JsonKey.BEST_SCORE: GameRule.INITIAL_BEST_SCORE,
                JsonKey.SCORE_HISTORY: [],
            }

        return {
            JsonKey.QUIZZES: [quiz.to_dict() for quiz in quizzes],
            JsonKey.BEST_SCORE: GameRule.INITIAL_BEST_SCORE,
            JsonKey.SCORE_HISTORY: [],
        }

    def save_state(self):
        """현재 상태를 state.json 파일에 저장한다."""
        state_data = {
            JsonKey.QUIZZES: [quiz.to_dict() for quiz in self.quizzes],
            JsonKey.BEST_SCORE: self.best_score,
            JsonKey.SCORE_HISTORY: self.score_history,
        }

        try:
            with open(self.state_file, "w", encoding=FileConfig.ENCODING) as file:
                json.dump(
                    state_data,
                    file,
                    ensure_ascii=False,
                    indent=FileConfig.JSON_INDENT,
                )
        except OSError:
            print(Text.STATE_SAVE_ERROR)

    def load_state(self):
        """state.json 또는 기본 퀴즈 파일에서 전체 상태를 불러온다."""
        state_data = self.load_json_file(self.state_file, None)

        if not isinstance(state_data, dict):
            state_data = self.create_initial_state_data()
            self.best_score = GameRule.INITIAL_BEST_SCORE
            self.score_history = []
            quizzes = self.create_quiz_objects(state_data[JsonKey.QUIZZES])
            self.quizzes = quizzes
            self.save_state()
            return quizzes

        quiz_data_list = state_data.get(JsonKey.QUIZZES, [])
        best_score = state_data.get(JsonKey.BEST_SCORE, GameRule.INITIAL_BEST_SCORE)
        score_history = state_data.get(JsonKey.SCORE_HISTORY, [])

        if not isinstance(quiz_data_list, list):
            print(Text.STATE_QUIZZES_TYPE_ERROR)
            state_data = self.create_initial_state_data()
            quiz_data_list = state_data[JsonKey.QUIZZES]

        if not isinstance(best_score, int):
            print(Text.STATE_BEST_SCORE_TYPE_ERROR)
            best_score = GameRule.INITIAL_BEST_SCORE

        if not isinstance(score_history, list):
            print(Text.STATE_HISTORY_TYPE_ERROR)
            score_history = []

        quizzes = self.create_quiz_objects(quiz_data_list)

        if not quizzes and quiz_data_list:
            print(Text.STATE_INVALID_QUIZ_DATA)
            state_data = self.create_initial_state_data()
            quiz_data_list = state_data[JsonKey.QUIZZES]
            quizzes = self.create_quiz_objects(quiz_data_list)
            best_score = GameRule.INITIAL_BEST_SCORE
            score_history = []

        self.best_score = best_score
        self.score_history = self.validate_score_history(score_history)
        self.quizzes = quizzes

        if not os.path.exists(self.state_file):
            self.save_state()

        return quizzes

    def validate_score_history(self, score_history):
        """점수 히스토리 목록을 검증하고 유효한 항목만 반환한다."""
        validated_history = []

        for entry in score_history:
            if not isinstance(entry, dict):
                continue

            played_at = entry.get(JsonKey.PLAYED_AT)
            question_count = entry.get(JsonKey.QUESTION_COUNT)
            correct_count = entry.get(JsonKey.CORRECT_COUNT)
            hint_used_count = entry.get(JsonKey.HINT_USED_COUNT)
            score = entry.get(JsonKey.SCORE)

            if not isinstance(played_at, str) or not played_at.strip():
                continue

            if not isinstance(question_count, int) or question_count < GameRule.MIN_SCORE:
                continue

            if not isinstance(correct_count, int) or correct_count < GameRule.MIN_SCORE:
                continue

            if not isinstance(hint_used_count, int) or hint_used_count < GameRule.MIN_SCORE:
                continue

            if not isinstance(score, int) or score < GameRule.MIN_SCORE:
                continue

            validated_history.append(
                {
                    JsonKey.PLAYED_AT: played_at.strip(),
                    JsonKey.QUESTION_COUNT: question_count,
                    JsonKey.CORRECT_COUNT: correct_count,
                    JsonKey.HINT_USED_COUNT: hint_used_count,
                    JsonKey.SCORE: score,
                }
            )

        return validated_history

    def record_score_history(self, question_count, correct_count, hint_used_count, score):
        """현재 플레이 결과를 점수 히스토리에 추가한다."""
        history_entry = {
            JsonKey.PLAYED_AT: datetime.now().strftime(GameRule.DATETIME_FORMAT),
            JsonKey.QUESTION_COUNT: question_count,
            JsonKey.CORRECT_COUNT: correct_count,
            JsonKey.HINT_USED_COUNT: hint_used_count,
            JsonKey.SCORE: score,
        }
        self.score_history.append(history_entry)

    def display_menu(self):
        """메인 메뉴를 출력한다."""
        print(Text.APP_TITLE)
        print(Text.MENU_PLAY_QUIZ)
        print(Text.MENU_ADD_QUIZ)
        print(Text.MENU_SHOW_QUIZ_LIST)
        print(Text.MENU_SHOW_SCORE)
        print(Text.MENU_DELETE_QUIZ)
        print(Text.MENU_EXIT)

    def get_menu_choice(self):
        """사용자에게 메뉴 번호를 입력받고 검증한다."""
        while True:
            try:
                raw_value = input(Text.MENU_PROMPT).strip()

                if not raw_value:
                    print(Text.EMPTY_MENU_INPUT)
                    continue

                choice = int(raw_value)

                if GameRule.MENU_MIN <= choice <= GameRule.MENU_MAX:
                    return choice

                print(Text.MENU_RANGE_ERROR)

            except ValueError:
                print(Text.NUMBER_ONLY)
            except KeyboardInterrupt:
                print(Text.INTERRUPT_MENU)
            except EOFError:
                print(Text.EOF_SAFE_EXIT)
                self.is_running = False
                return MenuOption.EXIT

    def get_answer_choice(self, quiz):
        """문제의 정답 번호를 입력받고 검증한다."""
        choice_count = len(quiz.choices)

        while True:
            try:
                raw_value = input(Text.ANSWER_PROMPT).strip()

                if not raw_value:
                    print(Text.EMPTY_ANSWER_INPUT)
                    continue

                answer = int(raw_value)

                if GameRule.CHOICE_MIN <= answer <= choice_count:
                    return answer

                print(Text.ANSWER_RANGE_TEMPLATE.format(max_value=choice_count))

            except ValueError:
                print(Text.NUMBER_ONLY)
            except KeyboardInterrupt:
                print(Text.INTERRUPT_ANSWER)
            except EOFError:
                print(Text.EOF_SAFE_EXIT)
                self.is_running = False
                return choice_count

    def get_non_empty_input(self, prompt):
        """비어 있지 않은 문자열 입력을 받는다."""
        while True:
            try:
                value = input(prompt).strip()

                if value:
                    return value

                print(Text.EMPTY_TEXT_INPUT)

            except KeyboardInterrupt:
                print(Text.INTERRUPT_RETRY)
            except EOFError:
                print(Text.EOF_SAFE_EXIT)
                self.is_running = False
                return ""

    def get_optional_input(self, prompt):
        """선택 입력 문자열을 받는다."""
        try:
            return input(prompt).strip()
        except KeyboardInterrupt:
            print(Text.INTERRUPT_HINT_SKIP)
            return ""
        except EOFError:
            print(Text.EOF_SAFE_EXIT)
            self.is_running = False
            return ""

    def get_choice_number_input(self, prompt, min_value, max_value):
        """지정된 범위의 숫자 입력을 받는다."""
        while True:
            try:
                raw_value = input(prompt).strip()

                if not raw_value:
                    print(Text.EMPTY_NUMBER_INPUT)
                    continue

                number = int(raw_value)

                if min_value <= number <= max_value:
                    return number

                print(
                    Text.NUMBER_RANGE_TEMPLATE.format(
                        min_value=min_value,
                        max_value=max_value,
                    )
                )

            except ValueError:
                print(Text.NUMBER_ONLY)
            except KeyboardInterrupt:
                print(Text.INTERRUPT_RETRY)
            except EOFError:
                print(Text.EOF_SAFE_EXIT)
                self.is_running = False
                return max_value

    def get_confirmation(self, prompt):
        """y/n 확인 입력을 받는다."""
        while True:
            try:
                value = input(prompt).strip().lower()

                if value in InputValue.YES_VALUES:
                    return True

                if value in InputValue.NO_VALUES:
                    return False

                print(Text.YES_NO_ONLY)

            except KeyboardInterrupt:
                print(Text.INTERRUPT_DELETE_CANCEL)
                return False
            except EOFError:
                print(Text.EOF_SAFE_EXIT)
                self.is_running = False
                return False

    def get_hint_usage(self, quiz):
        """힌트 사용 여부를 확인하고, 사용 시 힌트를 출력한다."""
        if not quiz.hint:
            return False

        is_confirmed = self.get_confirmation(Text.CONFIRM_HINT_PROMPT)

        if not self.is_running:
            return False

        if is_confirmed:
            print(Text.HINT_TEMPLATE.format(hint=quiz.hint))
            print(Text.HINT_PENALTY_TEMPLATE.format(penalty=self.hint_penalty))
            return True

        return False

    def get_randomized_quizzes(self):
        """현재 퀴즈 목록을 랜덤 순서로 섞어 반환한다."""
        return random.sample(self.quizzes, len(self.quizzes))

    def get_quiz_count_to_play(self, max_count):
        """플레이할 문제 수를 입력받는다."""
        print(Text.TOTAL_QUIZ_COUNT_TEMPLATE.format(max_count=max_count))
        return self.get_choice_number_input(
            Text.QUIZ_COUNT_PROMPT,
            GameRule.CHOICE_MIN,
            max_count,
        )

    def calculate_score(self, correct_count, total_count, hint_used_count):
        """정답 수와 힌트 사용 횟수를 바탕으로 최종 점수를 계산한다."""
        base_score = int((correct_count / total_count) * 100)
        penalty_score = hint_used_count * self.hint_penalty
        final_score = base_score - penalty_score
        return max(final_score, GameRule.MIN_SCORE)

    def update_best_score(self, score):
        """현재 점수와 최고 점수를 비교해 갱신한다."""
        if score > self.best_score:
            self.best_score = score
            print(Text.BEST_SCORE_UPDATED)

    def handle_menu(self, choice):
        """선택한 메뉴 번호에 따라 동작한다."""
        if choice == MenuOption.PLAY_QUIZ:
            self.play_quiz()
        elif choice == MenuOption.ADD_QUIZ:
            self.add_quiz()
        elif choice == MenuOption.SHOW_QUIZ_LIST:
            self.show_quiz_list()
        elif choice == MenuOption.SHOW_SCORE:
            self.show_score()
        elif choice == MenuOption.DELETE_QUIZ:
            self.delete_quiz()
        elif choice == MenuOption.EXIT:
            self.exit_game()

    def play_quiz(self):
        """등록된 퀴즈를 랜덤 순서로 출제하고 결과를 출력한다."""
        self.clear_screen()
        print(Text.SECTION_PLAY_QUIZ)

        if not self.quizzes:
            print(Text.NO_REGISTERED_QUIZ)
            self.pause()
            return

        max_count = len(self.quizzes)
        quiz_count = self.get_quiz_count_to_play(max_count)

        if not self.is_running:
            return

        randomized_quizzes = self.get_randomized_quizzes()
        quiz_list = randomized_quizzes[:quiz_count]

        correct_count = 0
        hint_used_count = 0
        total_count = len(quiz_list)

        for index, quiz in enumerate(quiz_list, start=1):
            self.clear_screen()
            print(Text.SECTION_PLAY_QUIZ)
            print(Text.PROGRESS_TEMPLATE.format(index=index, total_count=total_count))
            quiz.display()

            if self.get_hint_usage(quiz):
                hint_used_count += 1

            if not self.is_running:
                return

            user_answer = self.get_answer_choice(quiz)

            if not self.is_running:
                return

            if quiz.is_correct(user_answer):
                print(Text.CORRECT)
                correct_count += 1
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(Text.WRONG)
                print(
                    Text.CORRECT_ANSWER_TEMPLATE.format(
                        answer=quiz.answer,
                        correct_text=correct_text,
                    )
                )

            self.pause()

            if not self.is_running:
                return

        score = self.calculate_score(correct_count, total_count, hint_used_count)
        self.update_best_score(score)
        self.record_score_history(
            question_count=total_count,
            correct_count=correct_count,
            hint_used_count=hint_used_count,
            score=score,
        )
        self.save_state()

        self.clear_screen()
        print(Text.SECTION_QUIZ_RESULT)
        print(
            Text.RESULT_CORRECT_COUNT_TEMPLATE.format(
                correct_count=correct_count,
                total_count=total_count,
            )
        )
        print(Text.RESULT_HINT_USED_TEMPLATE.format(hint_used_count=hint_used_count))
        print(Text.RESULT_SCORE_TEMPLATE.format(score=score))
        print(Text.RESULT_BEST_SCORE_TEMPLATE.format(best_score=self.best_score))
        self.pause()

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가한다."""
        self.clear_screen()
        print(Text.SECTION_ADD_QUIZ)

        question = self.get_non_empty_input(Text.QUESTION_PROMPT)

        if not self.is_running:
            return

        choices = []

        for index in range(GameRule.CHOICE_MIN, GameRule.CHOICE_COUNT + 1):
            choice = self.get_non_empty_input(
                Text.CHOICE_PROMPT_TEMPLATE.format(index=index)
            )

            if not self.is_running:
                return

            choices.append(choice)

        answer = self.get_choice_number_input(
            Text.ANSWER_NUMBER_PROMPT,
            GameRule.CHOICE_MIN,
            GameRule.CHOICE_COUNT,
        )

        if not self.is_running:
            return

        hint = self.get_optional_input(Text.HINT_INPUT_PROMPT)

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

        print(Text.QUIZ_ADDED)
        print(Text.QUIZ_COUNT_TEMPLATE.format(quiz_count=len(self.quizzes)))
        self.pause()

    def show_quiz_list(self):
        """등록된 퀴즈 목록을 출력한다."""
        self.clear_screen()
        print(Text.SECTION_QUIZ_LIST)

        if not self.quizzes:
            print(Text.NO_REGISTERED_QUIZ)
            self.pause()
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

        self.pause()

    def show_score(self):
        """현재 최고 점수와 최근 점수 기록을 출력한다."""
        self.clear_screen()
        print(Text.SECTION_SHOW_SCORE)
        print(Text.RESULT_BEST_SCORE_TEMPLATE.format(best_score=self.best_score))

        if not self.score_history:
            print(Text.NO_SCORE_HISTORY)
            self.pause()
            return

        print(Text.RECENT_SCORE_HISTORY)
        recent_history = self.score_history[-GameRule.HISTORY_PREVIEW_LIMIT :]

        for index, history in enumerate(recent_history, start=1):
            print(
                Text.SCORE_HISTORY_TEMPLATE.format(
                    index=index,
                    played_at=history[JsonKey.PLAYED_AT],
                    question_count=history[JsonKey.QUESTION_COUNT],
                    correct_count=history[JsonKey.CORRECT_COUNT],
                    hint_used_count=history[JsonKey.HINT_USED_COUNT],
                    score=history[JsonKey.SCORE],
                )
            )

        self.pause()

    def delete_quiz(self):
        """퀴즈 번호를 받아 삭제하고 저장 파일에도 반영한다."""
        self.clear_screen()
        print(Text.SECTION_DELETE_QUIZ)

        if not self.quizzes:
            print(Text.NO_QUIZ_TO_DELETE)
            self.pause()
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

        quiz_number = self.get_choice_number_input(
            Text.QUIZ_DELETE_PROMPT,
            GameRule.CHOICE_MIN,
            len(self.quizzes),
        )

        if not self.is_running:
            return

        target_quiz = self.quizzes[quiz_number - 1]

        print(Text.SELECTED_QUIZ_TEMPLATE.format(question=target_quiz.question))
        is_confirmed = self.get_confirmation(Text.CONFIRM_DELETE_PROMPT)

        if not self.is_running:
            return

        if not is_confirmed:
            print(Text.DELETE_CANCELLED)
            self.pause()
            return

        deleted_quiz = self.quizzes.pop(quiz_number - 1)
        self.save_state()

        print(Text.QUIZ_DELETED)
        print(Text.DELETED_QUESTION_TEMPLATE.format(question=deleted_quiz.question))
        print(Text.QUIZ_COUNT_TEMPLATE.format(quiz_count=len(self.quizzes)))
        self.pause()

    def exit_game(self):
        """프로그램을 종료한다."""
        print(Text.EXIT_MESSAGE)
        self.is_running = False

    def run(self):
        """게임 메인 루프를 실행한다."""
        while self.is_running:
            self.clear_screen()
            self.display_menu()
            choice = self.get_menu_choice()

            if not self.is_running:
                break

            self.handle_menu(choice)