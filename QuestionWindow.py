from PyQt6 import QtCore, QtGui, QtWidgets
import logging
import random

logger = logging.getLogger(__name__)


class Ui_QuestionWindow(object):
    def setupUi(self, QuestionWindow):
        logger.info("Initializing QuestionWindow UI")
        try:
            QuestionWindow.setObjectName("QuestionWindow")
            QuestionWindow.resize(800, 600)
            self.centralwidget = QtWidgets.QWidget(parent=QuestionWindow)
            self.centralwidget.setObjectName("centralwidget")

            self.setup_buttons()
            self.setup_labels()
            self.setup_line_edit()
            self.setup_text_edit()

            QuestionWindow.setCentralWidget(self.centralwidget)
            self.retranslateUi(QuestionWindow)
            QtCore.QMetaObject.connectSlotsByName(QuestionWindow)
            logger.debug("QuestionWindow UI setup completed")
        except Exception as e:
            logger.error(f"Error during QuestionWindow setup: {str(e)}")
            raise

    def setup_buttons(self):
        font = self.get_button_font()

        self.exitBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.exitBt.setGeometry(QtCore.QRect(0, 0, 75, 24))
        self.exitBt.setFont(font)
        self.exitBt.setObjectName("exitBt")
        self.exitBt.clicked.connect(self.exit_and_return)

        self.answerA = QtWidgets.QPushButton(parent=self.centralwidget)
        self.answerA.setGeometry(QtCore.QRect(100, 270, 271, 121))
        self.answerA.setFont(font)
        self.answerA.setObjectName("answerA")
        self.answerA.clicked.connect(lambda: self.check_answer(self.answerA))

        self.answerB = QtWidgets.QPushButton(parent=self.centralwidget)
        self.answerB.setGeometry(QtCore.QRect(430, 270, 271, 121))
        self.answerB.setFont(font)
        self.answerB.setObjectName("answerB")
        self.answerB.clicked.connect(lambda: self.check_answer(self.answerB))

        self.answerC = QtWidgets.QPushButton(parent=self.centralwidget)
        self.answerC.setGeometry(QtCore.QRect(100, 440, 271, 121))
        self.answerC.setFont(font)
        self.answerC.setObjectName("answerC")
        self.answerC.clicked.connect(lambda: self.check_answer(self.answerC))

        self.answerD = QtWidgets.QPushButton(parent=self.centralwidget)
        self.answerD.setGeometry(QtCore.QRect(430, 440, 271, 121))
        self.answerD.setFont(font)
        self.answerD.setObjectName("answerD")
        self.answerD.clicked.connect(lambda: self.check_answer(self.answerD))

        self.answerBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.answerBt.setGeometry(QtCore.QRect(630, 270, 71, 121))
        self.answerBt.setFont(font)
        self.answerBt.setText("Submit")
        self.answerBt.setVisible(False)
        self.answerBt.clicked.connect(lambda: self.check_answer(self.answerText))

    def setup_labels(self):
        font = self.get_label_font()

        self.questionLb = QtWidgets.QLabel(parent=self.centralwidget)
        self.questionLb.setGeometry(QtCore.QRect(110, 40, 581, 181))
        self.questionLb.setFont(font)
        self.questionLb.setWordWrap(True)
        self.questionLb.setObjectName("questionLb")

        self.answerLb = QtWidgets.QLabel(parent=self.centralwidget)
        self.answerLb.setGeometry(QtCore.QRect(100, 400, 601, 200))
        self.answerLb.setFont(QtGui.QFont("Segoe UI", 12))
        self.answerLb.setStyleSheet("color: red;")
        self.answerLb.setVisible(False)
        self.answerLb.setWordWrap(True)
        self.answerLb.setObjectName("answerLb")

    def setup_line_edit(self):
        font = self.get_label_font()

        self.answerLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.answerLine.setGeometry(QtCore.QRect(100, 270, 601, 121))
        self.answerLine.setFont(font)
        self.answerLine.setVisible(False)
        self.answerLine.returnPressed.connect(lambda: self.check_answer(self.answerLine))

    def setup_text_edit(self):
        font = self.get_label_font()

        self.answerText = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.answerText.setGeometry(QtCore.QRect(100, 270, 521, 121))
        self.answerText.setFont(font)
        self.answerText.setVisible(False)

    def get_button_font(self):
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(12)
        font.setBold(True)
        return font

    def get_label_font(self):
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(12)
        font.setBold(True)
        return font

    def retranslateUi(self, QuestionWindow):
        _translate = QtCore.QCoreApplication.translate
        QuestionWindow.setWindowTitle(_translate("QuestionWindow", "MainWindow"))
        self.exitBt.setText(_translate("QuestionWindow", "Exit "))
        self.answerA.setText(_translate("QuestionWindow", "Placeholder A"))
        self.answerB.setText(_translate("QuestionWindow", "Placeholder B"))
        self.answerC.setText(_translate("QuestionWindow", "Placeholder C"))
        self.answerD.setText(_translate("QuestionWindow", "Placeholder D"))
        self.questionLb.setText(_translate("QuestionWindow", "Placeholder"))

    def load_questions(self, qa_list, parent_window, difficulty):
        logger.info(f"Loading questions for {difficulty} difficulty")
        try:
            self.parent_window = parent_window
            self.difficulty = difficulty
            self.correct_count = 0

            if difficulty == "easy":
                multi_choice, identification, enumeration = self.categorize_questions(qa_list)
                self.qa_list = multi_choice + identification + enumeration
            elif difficulty == "intermediate":
                multi_choice, identification, enumeration = self.categorize_questions(qa_list)
                random.shuffle(multi_choice)
                random.shuffle(identification)
                random.shuffle(enumeration)
                self.qa_list = multi_choice + identification + enumeration
            elif difficulty == "hard":
                random.shuffle(qa_list)
                self.qa_list = qa_list

            logger.info(f"Total questions loaded: {len(self.qa_list)}")
            self.current_index = 0
            self.show_question()
        except Exception as e:
            logger.error(f"Error loading questions: {str(e)}")
            raise

    def categorize_questions(self, qa_list):
        multi_choice = []
        identification = []
        enumeration = []
        for qa in qa_list:
            if qa[2] == "multi":
                multi_choice.append(qa)
            elif qa[2] == "iden":
                identification.append(qa)
            elif qa[2] == "enum":
                enumeration.append(qa)
        return multi_choice, identification, enumeration

    def show_question(self):
        logger.info("Showing questions")
        try:
            if self.current_index >= len(self.qa_list):
                self.show_finish_dialog()
                return

            question_data = self.qa_list[self.current_index]
            question = question_data[0]
            correct_answer = question_data[1]
            question_type = question_data[2] if len(question_data) > 2 else "iden"

            self.questionLb.setText(question)
            self.display_answer_input(question_type, correct_answer)
            logger.debug(f"Showing question {self.current_index + 1} of {len(self.qa_list)}")
        except Exception as e:
            logger.error(f"Error showing questions: {str(e)}")
            raise

    def display_answer_input(self, question_type, correct_answer):
        if question_type == "multi":
            self.setup_multiple_choice(correct_answer)
        elif question_type == "iden":
            self.answerLine.setFocus()
            self.answerA.setVisible(False)
            self.answerB.setVisible(False)
            self.answerC.setVisible(False)
            self.answerD.setVisible(False)
            self.answerLine.setVisible(True)
            self.answerLine.clear()
            logger.debug(f"Question type: {question_type}, Correct answer: '{correct_answer}'")
        elif question_type == "enum":
            self.answerText.setFocus()
            self.answerA.setVisible(False)
            self.answerB.setVisible(False)
            self.answerC.setVisible(False)
            self.answerD.setVisible(False)
            self.answerLine.setVisible(False)
            self.answerText.setVisible(True)
            self.answerBt.setVisible(True)
            self.answerText.clear()
            logger.debug(f"Question type: {question_type}, Correct answer: '{correct_answer}'")

    def setup_multiple_choice(self, correct_answer):
        self.answerA.setVisible(True)
        self.answerB.setVisible(True)
        self.answerC.setVisible(True)
        self.answerD.setVisible(True)
        self.answerLine.setVisible(False)
        self.answerText.setVisible(False)
        self.answerBt.setVisible(False)

        possible_answers = [qa[1] for qa in self.qa_list if qa[2] in ["multi", "iden"] and qa[1] != correct_answer]
        unique_answers = list(set(possible_answers))

        answers = [correct_answer]
        if unique_answers:
            answers += random.sample(unique_answers, min(3, len(unique_answers)))

        default_options = ["Option 1", "Option 2", "Option 3"]
        while len(answers) < 4 and default_options:
            answers.append(default_options.pop())

        while len(answers) < 4:
            answers.append(f"Option {len(answers) + 1}")

        random.shuffle(answers)
        self.answerA.setText(answers[0])
        self.answerB.setText(answers[1])
        self.answerC.setText(answers[2])
        self.answerD.setText(answers[3])
        logger.debug(f"Question type: multi, Correct answer: '{correct_answer}'")

    def normalize_enumeration(self, answer):
        lines = [line.strip() for line in answer.split('\n') if line.strip()]
        return '\n'.join(sorted(lines))

    def validate_answer(self, answer, question_type):
        if question_type == "enum":
            return bool(answer.strip())
        return len(answer.strip()) > 0

    def check_answer(self, source):
        if hasattr(self, '_processing_answer') and self._processing_answer:
            return
        self._processing_answer = True
        try:
            question, correct_answer, question_type = self.qa_list[self.current_index]
            user_answer = self.get_user_answer(source, question_type)

            if not user_answer:
                logger.warning("Empty answer submitted")
                self.answerLb.setText("Please enter an answer!")
                self.answerLb.setVisible(True)
                return

            logger.debug(f"User answer: '{user_answer}', Correct answer: '{correct_answer}'")
            is_correct = self.is_correct_answer(user_answer, correct_answer, question_type)

            if is_correct:
                self.correct_count += 1
                self.answerLb.setVisible(False)
                self.handle_correct_answer(source)
                logger.debug("Correct answer")
            else:
                self.handle_incorrect_answer(source, correct_answer, question_type)
                logger.debug("Incorrect answer")
        except Exception as e:
            logger.error(f"Error checking answer: {str(e)}", exc_info=True)
            raise
        finally:
            self._processing_answer = False

    def get_user_answer(self, source, question_type):
        if question_type == "multi":
            return source.text().strip()
        elif question_type == "iden":
            return self.answerLine.text().strip()
        elif question_type == "enum":
            return self.answerText.toPlainText().strip()

    def is_correct_answer(self, user_answer, correct_answer, question_type):
        if question_type == "enum":
            user_lines = sorted(line.strip() for line in user_answer.split('\n') if line.strip())
            correct_lines = sorted(line.strip() for line in correct_answer.split('\n') if line.strip())
            return user_lines == correct_lines
        return user_answer.lower() == correct_answer.lower()

    def handle_correct_answer(self, source):
        if self.difficulty == "easy":
            source.setStyleSheet("background-color: green")
            QtCore.QTimer.singleShot(1000, self.next_question)
        elif self.difficulty == "intermediate":
            source.setStyleSheet("background-color: green")
            QtCore.QTimer.singleShot(1500, self.next_question)
        elif self.difficulty == "hard":
            self.next_question()

    def handle_incorrect_answer(self, source, correct_answer, question_type):
        if question_type == "multi":
            for b in [self.answerA, self.answerB, self.answerC, self.answerD]:
                if b.text() == correct_answer:
                    b.setStyleSheet("background-color: green")
                elif b == source:
                    b.setStyleSheet("background-color: red")
        else:
            self.answerLb.setText(f"Correct answer: {correct_answer}")
            self.answerLb.setVisible(True)

        if self.difficulty == "easy":
            if question_type == "multi":
                source.setStyleSheet("background-color: red")
        elif self.difficulty == "intermediate":
            if question_type == "multi":
                for b in [self.answerA, self.answerB, self.answerC, self.answerD]:
                    if b.text() == correct_answer:
                        b.setStyleSheet("background-color: green")
                    else:
                        b.setStyleSheet("")
            else:
                source.setStyleSheet("background-color: red")
            QtCore.QTimer.singleShot(1500, self.next_question)
        elif self.difficulty == "hard":
            self.next_question()

    def next_question(self):
        logger.info("Going to next question")
        try:
            self.answerLb.setVisible(False)
            self.current_index += 1
            self.reset_buttons()
            self.show_question()
            logger.debug("Next Question")
        except Exception as e:
            logger.error(f"Error showing next question: {str(e)}")
            raise

    def reset_buttons(self):
        for button in [self.answerA, self.answerB, self.answerC, self.answerD]:
            button.setStyleSheet("")
        self.answerLine.setStyleSheet("")
        self.answerText.setStyleSheet("")

    def show_finish_dialog(self):
        percentage = (self.correct_count / len(self.qa_list)) * 100
        logger.info(f"Quiz completed - Score: {self.correct_count}/{len(self.qa_list)} ({percentage:.1f}%)")
        try:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText(
                f"Quiz finished! You scored {self.correct_count}/{len(self.qa_list)}. Do you want to retake the quiz?")
            msg.setWindowTitle("Quiz Finished")
            msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            ret = msg.exec()

            if ret == QtWidgets.QMessageBox.StandardButton.Yes:
                self.current_index = 0
                self.correct_count = 0
                self.reset_buttons()
                self.show_question()
                logger.debug("Retaking Quiz")
            else:
                self.centralwidget.window().close()
                logger.debug("Exiting Quiz")
        except Exception as e:
            logger.error(f"Error showing finish dialog: {str(e)}")
            raise

    def exit_and_return(self):
        logger.info("Returning to main window")
        try:
            self.parent_window.MultipleChoiceWindow.show()
            self.centralwidget.window().close()
            logger.info("User exited to main window")
        except Exception as e:
            logger.error(f"Error returning to main window: {str(e)}")
            raise


if __name__ == "__main__":
    import sys

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    QuestionWindow = QtWidgets.QMainWindow()
    ui = Ui_QuestionWindow()
    ui.setupUi(QuestionWindow)
    QuestionWindow.show()
    sys.exit(app.exec())