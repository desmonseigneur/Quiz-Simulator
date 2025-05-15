from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QKeyEvent
import logging
from logging_utils import setup_logging, log_exception
from QuestionWindow import Ui_QuestionWindow
import json
import os
import sys

logger = logging.getLogger(__name__)
qt_log_handler = setup_logging()
sys.excepthook = log_exception

class Ui_MultipleChoiceWindow(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.MultipleChoiceWindow = None
        self.centralwidget = None
        self.idenMultiBt = None
        self.enuBt = None
        self.addBt = None
        self.saveBt = None
        self.loadBt = None
        self.clearBt = None
        self.proceedBt = None
        self.questionLb = None
        self.answerLb = None
        self.questionLine = None
        self.answerLine = None
        self.answerText = None
        self.qaLV = None
        self.model = None
        self.active_button = None
        self.data_dir = None
        self.qa_list = None
        self.easyRb = None
        self.intermediateRb = None
        self.hardRb = None
        
    def setupUi(self, MultipleChoiceWindow):
        logger.info("Initializing MultipleChoiceWindow UI")
        try:
            self.MultipleChoiceWindow = MultipleChoiceWindow
            MultipleChoiceWindow.setObjectName("MultipleChoiceWindow")
            MultipleChoiceWindow.setFixedSize(801, 600)
            self.centralwidget = QtWidgets.QWidget(parent=MultipleChoiceWindow)
            self.centralwidget.setObjectName("centralwidget")

            self.setup_buttons()
            self.setup_labels()
            self.setup_line_edit()
            self.setup_text_edit()
            self.setup_list_view()

            MultipleChoiceWindow.setCentralWidget(self.centralwidget)
            self.retranslateUi(MultipleChoiceWindow)
            QtCore.QMetaObject.connectSlotsByName(MultipleChoiceWindow)

            # Initialize data directory
            self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)

            # Connect key press event
            self.qaLV.keyPressEvent = self.keyPressEvent

            # Connect drag and drop events
            self.qaLV.startDrag = self.startDrag
            self.qaLV.dragEnterEvent = self.dragEnterEvent
            self.qaLV.dragMoveEvent = self.dragMoveEvent
            self.qaLV.dropEvent = self.dropEvent

            logger.debug("UI setup completed successfully")
        except Exception as e:
            logger.error(f"Error during UI setup: {str(e)}")
            raise

    def setup_buttons(self):
        font = self.get_button_font()

        self.idenMultiBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.idenMultiBt.setGeometry(QtCore.QRect(10, 20, 100, 40))
        self.idenMultiBt.setFont(font)
        self.idenMultiBt.setObjectName("idenMultiBt")
        self.idenMultiBt.clicked.connect(lambda: self.set_button_state("idenMultiBt"))

        self.enuBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.enuBt.setGeometry(QtCore.QRect(10, 70, 100, 40))
        self.enuBt.setFont(font)
        self.enuBt.setObjectName("enuBt")
        self.enuBt.clicked.connect(lambda: self.set_button_state("enuBt"))

        self.addBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addBt.setGeometry(QtCore.QRect(660, 30, 111, 51))
        self.addBt.setFont(font)
        self.addBt.setObjectName("addBt")
        self.addBt.clicked.connect(self.add_qa)

        self.saveBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.saveBt.setGeometry(QtCore.QRect(10, 560, 81, 31))
        self.saveBt.setFont(font)
        self.saveBt.setObjectName("saveBt")
        self.saveBt.clicked.connect(self.save_qa)

        self.loadBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadBt.setGeometry(QtCore.QRect(100, 560, 81, 31))
        self.loadBt.setFont(font)
        self.loadBt.setObjectName("loadBt")
        self.loadBt.clicked.connect(self.load_qa)

        self.clearBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.clearBt.setGeometry(QtCore.QRect(190, 560, 81, 31))
        self.clearBt.setFont(font)
        self.clearBt.setObjectName("clearBt")
        self.clearBt.clicked.connect(self.clear_qa)

        self.proceedBt = QtWidgets.QPushButton(parent=self.centralwidget)
        self.proceedBt.setGeometry(QtCore.QRect(710, 560, 81, 31))
        self.proceedBt.setFont(font)
        self.proceedBt.setObjectName("proceedBt")
        self.proceedBt.clicked.connect(self.show_difficulty_dialog)

    def setup_labels(self):
        font = self.get_label_font()

        self.questionLb = QtWidgets.QLabel(parent=self.centralwidget)
        self.questionLb.setGeometry(QtCore.QRect(118, 28, 81, 16))
        self.questionLb.setFont(font)
        self.questionLb.setObjectName("questionLb")

        self.answerLb = QtWidgets.QLabel(parent=self.centralwidget)
        self.answerLb.setGeometry(QtCore.QRect(128, 68, 81, 16))
        self.answerLb.setFont(font)
        self.answerLb.setObjectName("answerLb")

    def setup_line_edit(self):
        font = self.get_label_font()

        self.questionLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.questionLine.setGeometry(QtCore.QRect(200, 20, 441, 31))
        self.questionLine.setFont(font)
        self.questionLine.setObjectName("questionLine")

        self.answerLine = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.answerLine.setGeometry(QtCore.QRect(200, 60, 441, 31))
        self.answerLine.setFont(font)
        self.answerLine.setObjectName("answerLine")
        self.answerLine.returnPressed.connect(self.on_answer_entered)

    def setup_text_edit(self):
        font = self.get_label_font()

        self.answerText = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.answerText.setGeometry(QtCore.QRect(200, 60, 441, 80))
        self.answerText.setFont(font)
        self.answerText.setObjectName("answerText")
        self.answerText.setVisible(False)

    def setup_list_view(self):
        font = self.get_label_font()

        self.qaLV = QtWidgets.QListView(parent=self.centralwidget)
        self.qaLV.setGeometry(QtCore.QRect(0, 130, 801, 410))
        self.qaLV.setFont(font)
        self.qaLV.setObjectName("qaLV")
        self.model = QStandardItemModel()
        self.qaLV.setModel(self.model)
        self.qaLV.setSpacing(5)

        # Enable drag and drop
        self.qaLV.setDragEnabled(True)
        self.qaLV.setAcceptDrops(True)
        self.qaLV.setDropIndicatorShown(True)
        self.qaLV.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.qaLV.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        # Enable automatic scrolling during drag
        self.qaLV.setAutoScroll(True)

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

    def retranslateUi(self, MultipleChoiceWindow):
        _translate = QtCore.QCoreApplication.translate
        MultipleChoiceWindow.setWindowTitle(_translate("MultipleChoiceWindow", "MainWindow"))
        self.addBt.setText(_translate("MultipleChoiceWindow", "Add Q&A"))
        self.saveBt.setText(_translate("MultipleChoiceWindow", "Save Q&A"))
        self.loadBt.setText(_translate("MultipleChoiceWindow", "Load Q&A"))
        self.clearBt.setText(_translate("MultipleChoiceWindow", "Clear QA"))
        self.proceedBt.setText(_translate("MultipleChoiceWindow", "Proceed"))
        self.questionLb.setText(_translate("MultipleChoiceWindow", "Question:"))
        self.answerLb.setText(_translate("MultipleChoiceWindow", "Answer:"))
        self.idenMultiBt.setText(_translate("MultipleChoiceWindow", "Iden/Multi"))
        self.enuBt.setText(_translate("MultipleChoiceWindow", "Enumeration"))

    def set_button_state(self, button_name):
        logger.debug(f"Setting button state: {button_name}")
        try:
            self.idenMultiBt.setStyleSheet("")
            self.enuBt.setStyleSheet("")

            if button_name == "idenMultiBt":
                self.idenMultiBt.setStyleSheet("background-color: green")
                self.active_button = "idenMultiBt"
                self.answerLine.setVisible(True)
                self.answerText.setVisible(False)
            elif button_name == "enuBt":
                self.enuBt.setStyleSheet("background-color: green")
                self.active_button = "enuBt"
                self.answerLine.setVisible(False)
                self.answerText.setVisible(True)
        except Exception as e:
            logger.error(f"Error in set_button_state: {str(e)}")
            raise

    def add_qa(self):
        logger.debug("Adding new Q&A")
        try:
            question = self.questionLine.text()
            if not question:
                return

            if self.active_button == "enuBt":
                answer = self.answerText.toPlainText().strip()
                if answer:
                    qa_text = f"Q: {question}\nA: {answer}"
                    item = QStandardItem(qa_text)
                    item.setData("enum", QtCore.Qt.ItemDataRole.UserRole)  # For enumeration
                    self.model.appendRow(item)
                    self.questionLine.clear()
                    self.answerText.clear()
            else:
                answer = self.answerLine.text()
                if answer:
                    qa_text = f"Q: {question}\nA: {answer}"
                    item = QStandardItem(qa_text)
                    # Set type based on active button
                    if self.active_button == "idenMultiBt":
                        item.setData("multi", QtCore.Qt.ItemDataRole.UserRole)  # For multiple choice
                    else:
                        item.setData("iden", QtCore.Qt.ItemDataRole.UserRole)  # For identification
                    self.model.appendRow(item)
                    self.questionLine.clear()
                    self.answerLine.clear()
            logger.info(f"Added new Q&A: {question[:50]}...")
        except Exception as e:
            logger.error(f"Error adding Q&A - Question: '{question[:50]}...', Error: {str(e)}", exc_info=True)
            raise

    def keyPressEvent(self, event: QKeyEvent):
        try:
            if event.key() == QtCore.Qt.Key.Key_Delete:
                logger.debug("Delete key pressed")
                selected = self.qaLV.selectedIndexes()

                if not selected:
                    logger.debug("No Q&A selected for deletion")
                    return

                index = selected[0]
                item = self.model.itemFromIndex(index)

                if not item:
                    logger.error("Failed to get item from index")
                    return

                question_text = item.text().split('\n')[0][3:]  # Extract question part
                logger.info(f"Attempting to delete Q&A: {question_text[:50]}...")

                # Show confirmation dialog
                reply = QtWidgets.QMessageBox.question(
                    self.MultipleChoiceWindow,
                    "Delete Q&A",
                    "Are you sure you want to delete this Q&A from the list?",
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                    QtWidgets.QMessageBox.StandardButton.No
                )

                if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                    logger.debug("User confirmed deletion")
                    row = index.row()
                    self.model.removeRow(row)
                    logger.info(f"Deleted Q&A at row {row}: {question_text[:50]}...")
                    logger.debug(f"Remaining Q&A count: {self.model.rowCount()}")
                else:
                    logger.debug("User cancelled deletion")
            else:
                logger.debug(f"Key pressed: {event.key()} (not Delete)")
                super().keyPressEvent(event)

        except Exception as e:
            logger.error(f"Error in keyPressEvent: {str(e)}", exc_info=True)
            raise

    def startDrag(self, supportedActions):
        try:
            logger.debug("Starting drag operation")
            drag = QtGui.QDrag(self)
            mimeData = QMimeData()
            drag.setMimeData(mimeData)

            selected = self.qaLV.selectedIndexes()
            if selected:
                index = selected[0]
                item = self.model.itemFromIndex(index)
                if item:
                    question_text = item.text().split('\n')[0][3:]  # Extract question part
                    logger.info(f"Dragging Q&A: {question_text[:50]}... (row {index.row()})")

            result = drag.exec(QtCore.Qt.DropAction.MoveAction)
            logger.debug(f"Drag operation completed with result: {result}")
        except Exception as e:
            logger.error(f"Error in startDrag: {str(e)}", exc_info=True)
            raise

    def dragEnterEvent(self, event):
        try:
            logger.debug("Drag enter event triggered")
            if event.source() == self:
                logger.debug("Accepting drag enter event (internal source)")
                event.accept()
            else:
                logger.debug("Ignoring drag enter event (external source)")
                event.ignore()
        except Exception as e:
            logger.error(f"Error in dragEnterEvent: {str(e)}", exc_info=True)
            raise

    def dragMoveEvent(self, event):
        try:
            logger.debug("Drag move event triggered")
            if event.source() == self:
                logger.debug("Accepting drag move event")
                event.setDropAction(QtCore.Qt.DropAction.MoveAction)
                event.accept()

                # Log position information
                pos = event.position().toPoint()
                row = self.qaLV.indexAt(pos).row()
                logger.debug(f"Current drag position - Row: {row}, Coordinates: {pos.x()}, {pos.y()}")
            else:
                logger.debug("Ignoring drag move event (external source)")
                event.ignore()
        except Exception as e:
            logger.error(f"Error in dragMoveEvent: {str(e)}", exc_info=True)
            raise

    def dropEvent(self, event):
        try:
            logger.debug("Drop event triggered")
            if event.source() == self:
                logger.debug("Processing internal drop event")
                event.setDropAction(QtCore.Qt.DropAction.MoveAction)
                event.accept()

                # Get drop position
                pos = event.position().toPoint()
                drop_row = self.qaLV.indexAt(pos).row()
                if drop_row == -1:  # Below last item
                    drop_row = self.model.rowCount()
                    logger.debug(f"Dropping at end of list (new row {drop_row})")
                else:
                    logger.debug(f"Dropping at row {drop_row}")

                # Get dragged item
                selected = self.qaLV.selectedIndexes()
                if selected:
                    drag_row = selected[0].row()
                    item = self.model.itemFromIndex(selected[0])
                    question_text = item.text().split('\n')[0][3:]  # Extract question part

                    logger.info(f"Moving Q&A: {question_text[:50]}... from row {drag_row} to row {drop_row}")

                    # Move the item
                    items = self.model.takeRow(drag_row)
                    adjusted_drop_row = drop_row if drop_row < drag_row else drop_row - 1
                    self.model.insertRow(adjusted_drop_row, items)

                    # Select the moved item
                    self.qaLV.setCurrentIndex(self.model.index(adjusted_drop_row, 0))
                    logger.debug(f"Move completed. New position: row {adjusted_drop_row}")

                    # Log the new order
                    logger.debug("Current Q&A order after move:")
                    for i in range(min(3, self.model.rowCount())):  # Log first 3 items as sample
                        item = self.model.item(i)
                        if item:
                            logger.debug(f"Row {i}: {item.text().split('\n')[0][:30]}...")
            else:
                logger.debug("Ignoring external drop event")
                event.ignore()
        except Exception as e:
            logger.error(f"Error in dropEvent: {str(e)}", exc_info=True)
            raise

    def save_qa(self):
        logger.debug("Saving Q&A set")
        try:
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.MultipleChoiceWindow, "Save Q&A", self.data_dir, "JSON Files (*.json)"
            )
            if filepath:
                if not filepath.endswith(".json"):
                    filepath += ".json"

                qa_list = []
                for row in range(self.model.rowCount()):
                    item = self.model.item(row)
                    if item is not None:
                        qa_text = item.text()
                        question, answer = qa_text.split('\nA: ')
                        question = question[3:]
                        question_type = item.data(QtCore.Qt.ItemDataRole.UserRole)
                        # Map internal types to saved types
                        type_map = {
                            "multi": "multiple",
                            "iden": "identification",
                            "enum": "enumeration"
                        }
                        qa_list.append({
                            "question": question,
                            "answer": answer,
                            "type": question_type  # Save the original type ("multi", "iden", or "enum")
                        })

                with open(filepath, "w") as f:
                    json.dump(qa_list, f, indent=4)
                logger.info(f"Saved Q&A to {filepath}")
        except Exception as e:
            logger.error(f"Error Saving Q&A: {str(e)}")
            raise

    def load_qa(self):
        logger.debug("Loading Q&A set")
        try:
            filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.MultipleChoiceWindow, "Load Q&A", self.data_dir, "JSON Files (*.json)"
            )
            if filepath:
                self.model.clear()
                with open(filepath, "r") as f:
                    qa_list = json.load(f)
                    if not isinstance(qa_list, list):
                        logger.error("Invalid Q&A file format")
                        raise ValueError("Invalid Q&A file format")

                    for qa in qa_list:
                        qa_text = f"Q: {qa['question']}\nA: {qa['answer']}"
                        item = QStandardItem(qa_text)
                        # Map saved types back to internal types
                        type_map = {
                            "multiple": "multi",
                            "identification": "iden",
                            "enumeration": "enum"
                        }
                        item.setData(
                            type_map.get(qa["type"], qa["type"]),  # Fallback to original if not found
                            QtCore.Qt.ItemDataRole.UserRole
                        )
                        self.model.appendRow(item)

                logger.info(f"Loaded {len(qa_list)} Q&A items from {filepath}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error Loading Q&A: {str(e)}")
            raise

    def clear_qa(self):
        count = self.model.rowCount()
        reply = QtWidgets.QMessageBox.question(
            self.MultipleChoiceWindow, "Clear Q&A", "All questions will be deleted. Continue?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            logger.info(f"Clearing {count} Q&A items")
            self.model.clear()

    def show_difficulty_dialog(self):
        logger.debug("Choosing Q&A difficulty")
        try:
            dialog = QtWidgets.QDialog(self.MultipleChoiceWindow)
            dialog.setWindowTitle("Select Difficulty")
            dialog.setFixedSize(300, 150)

            layout = QtWidgets.QVBoxLayout()

            self.easyRb = QtWidgets.QRadioButton("Easy")
            self.intermediateRb = QtWidgets.QRadioButton("Intermediate")
            self.hardRb = QtWidgets.QRadioButton("Hard")

            layout.addWidget(self.easyRb)
            layout.addWidget(self.intermediateRb)
            layout.addWidget(self.hardRb)

            buttonBox = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttonBox.accepted.connect(dialog.accept)
            buttonBox.rejected.connect(dialog.reject)

            layout.addWidget(buttonBox)
            dialog.setLayout(layout)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                if self.easyRb.isChecked():
                    difficulty = "easy"
                elif self.intermediateRb.isChecked():
                    difficulty = "intermediate"
                elif self.hardRb.isChecked():
                    difficulty = "hard"
                else:
                    return

                # Prepare the question list
                self.qa_list = []
                for row in range(self.model.rowCount()):
                    item = self.model.item(row)
                    if item is not None:
                        qa_text = item.text()
                        question, answer = qa_text.split('\nA: ')
                        question = question[3:]  # Remove "Q: " prefix
                        question_type = item.data(QtCore.Qt.ItemDataRole.UserRole)

                        # For idenMultiBt questions, we'll add both types
                        if question_type == "multi":
                            # Add as identification
                            self.qa_list.append((question, answer, "iden"))
                            # Add as multiple choice
                            self.qa_list.append((question, answer, "multi"))
                        else:
                            self.qa_list.append((question, answer, question_type))

                self.question_window = QtWidgets.QMainWindow()
                self.ui_question = Ui_QuestionWindow()
                self.ui_question.setupUi(self.question_window)
                self.ui_question.load_questions(self.qa_list, self, difficulty)
                self.question_window.show()
                self.MultipleChoiceWindow.close()
                logger.info(f"User selected {difficulty} difficulty with {len(self.qa_list)} questions")
        except Exception as e:
            logger.error(f"Error Choosing difficulty: {str(e)}")
            raise

    def on_answer_entered(self):
        if self.answerLine.text().strip():
            self.add_qa()
            self.questionLine.setFocus()

    def load_questions(self, qa_list):
        logger.debug("Choosing Q&A difficulty")
        try:
            """Load questions from the question window back into the main window."""
            self.model.clear()
            for question, answer in qa_list:
                qa_text = f"Q: {question}\nA: {answer}"
                item = QStandardItem(qa_text)
                item.setData("iden", QtCore.Qt.ItemDataRole.UserRole)  # Changed from "idenBt"
            logger.info("Going back to first window successful.")
        except Exception as e:
            logger.error(f"Error Going back to first window: {str(e)}")
            raise

if __name__ == "__main__":
    from pathlib import Path  # Import Path from pathlib

    app = QtWidgets.QApplication(sys.argv)

    # Set the application icon (for the taskbar)
    icon_path = Path(__file__).with_name("icon.ico")  # Ensure the icon file is in the same directory as the script
    app.setWindowIcon(QtGui.QIcon(str(icon_path)))

    MultipleChoiceWindow = QtWidgets.QMainWindow()
    ui = Ui_MultipleChoiceWindow()
    ui.setupUi(MultipleChoiceWindow)

    # Set the window icon (for the title bar)
    MultipleChoiceWindow.setWindowIcon(QtGui.QIcon(str(icon_path)))

    MultipleChoiceWindow.show()
    sys.exit(app.exec())