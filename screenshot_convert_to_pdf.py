# 관련 패키지 설치
# pip install pyautogui pillow reportlab pyinstaller PyQt5

import sys
import time
import pyautogui
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QRadioButton, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QButtonGroup, QDesktopWidget

class ConvertPdfApp(QWidget):
    def __init__(self):
        super().__init__()
        self.count_down = 5 # 처음 타이머 시간
        self.user_delay = 3 # 사용자 마우스 이동 대기시간
        self.top_left_x = 0
        self.top_left_y = 0
        self.bottom_right_x = 0
        self.bottom_right_y = 0
        self.total_pages = 0
        self.current_page = 0
        self.initUI()

    def initUI(self):
        # 좌상단 좌표 설정 버튼
        self.top_left_label = QLabel('좌상단 좌표:')
        self.left_x_input = QLineEdit(self)
        self.left_y_input = QLineEdit(self)
        self.left_x_input.setPlaceholderText("x 좌표")
        self.left_y_input.setPlaceholderText("y 좌표")
        self.top_left_button = QPushButton('좌상단 좌표 설정', self)
        self.top_left_button.clicked.connect(self.set_left_top_coordinates)

        # 우하단 좌표 설정 버튼
        self.bottom_right_label = QLabel('우하단 좌표:')
        self.right_x_input = QLineEdit(self)
        self.right_y_input = QLineEdit(self)
        self.right_x_input.setPlaceholderText("x 좌표")
        self.right_y_input.setPlaceholderText("y 좌표")
        self.bottom_right_button = QPushButton('우하단 좌표 설정', self)
        self.bottom_right_button.clicked.connect(self.set_right_bottom_coordinates)

        # 다음 페이지 방향키 라디오 버튼
        self.next_button_label = QLabel('다음 페이지 방향키:')
        self.up_radio = QRadioButton('위', self)
        self.down_radio = QRadioButton('아래', self)
        self.left_radio = QRadioButton('왼쪽', self)
        self.right_radio = QRadioButton('오른쪽', self)

        # 라디오 버튼 그룹
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.up_radio)
        self.radio_group.addButton(self.down_radio)
        self.radio_group.addButton(self.left_radio)
        self.radio_group.addButton(self.right_radio)

        # PDF 파일명 입력
        self.pdf_label = QLabel('PDF 파일명:')
        self.pdf_input = QLineEdit(self)

        # 총 페이지 수 입력
        self.total_pages_label = QLabel('총 페이지 수:')
        self.total_pages_input = QLineEdit(self)

        # 실행 버튼
        self.run_button = QPushButton('PDF 파일 만들기', self)
        self.run_button.clicked.connect(self.run_screenshot_to_pdf)

        # 레이아웃 설정
        layout = QVBoxLayout()

        # 좌상단 좌표 설정 레이아웃
        top_left_layout = QHBoxLayout()
        top_left_layout.addWidget(self.top_left_label)
        top_left_layout.addWidget(self.left_x_input)
        top_left_layout.addWidget(self.left_y_input)
        top_left_layout.addWidget(self.top_left_button)
        layout.addLayout(top_left_layout)

        # 우하단 좌표 설정 레이아웃
        bottom_right_layout = QHBoxLayout()
        bottom_right_layout.addWidget(self.bottom_right_label)
        bottom_right_layout.addWidget(self.right_x_input)
        bottom_right_layout.addWidget(self.right_y_input)
        bottom_right_layout.addWidget(self.bottom_right_button)
        layout.addLayout(bottom_right_layout)

        # 라디오 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.next_button_label)
        button_layout.addWidget(self.up_radio)
        button_layout.addWidget(self.down_radio)
        button_layout.addWidget(self.left_radio)
        button_layout.addWidget(self.right_radio)
        layout.addLayout(button_layout)

        # PDF 파일명 입력 레이아웃
        pdf_layout = QHBoxLayout()
        pdf_layout.addWidget(self.pdf_label)
        pdf_layout.addWidget(self.pdf_input)
        layout.addLayout(pdf_layout)

        # 총 페이지 수 입력 레이아웃
        total_pages_layout = QHBoxLayout()
        total_pages_layout.addWidget(self.total_pages_label)
        total_pages_layout.addWidget(self.total_pages_input)
        layout.addLayout(total_pages_layout)

        # 실행 버튼 추가
        layout.addWidget(self.run_button)

        self.setLayout(layout)
        self.setWindowTitle('Screenshot convert to PDF')
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_left_top_coordinates(self):
        QMessageBox.information(self, '알림', '좌상단 좌표를 설정하려면 브라우저에서 원하는 위치로 이동하세요.')
        time.sleep(self.user_delay)  # 사용자에게 이동 시간을 주기 위해 대기
        self.top_left_x, self.top_left_y = pyautogui.position()
        self.left_x_input.setText(str(self.top_left_x))
        self.left_y_input.setText(str(self.top_left_y))
        QMessageBox.information(self, '좌표 설정 완료', f'좌상단 좌표가 ({self.top_left_x}, {self.top_left_y})로 설정되었습니다.')
        print(f"x, y coordinates set to: ({self.top_left_x}, {self.top_left_y})")

    def set_right_bottom_coordinates(self):
        QMessageBox.information(self, '알림', '우하단 좌표를 설정하려면 브라우저에서 원하는 위치로 이동하세요.')
        time.sleep(self.user_delay)  # 사용자에게 이동 시간을 주기 위해 대기
        self.bottom_right_x, self.bottom_right_y = pyautogui.position()
        self.right_x_input.setText(str(self.bottom_right_x))
        self.right_y_input.setText(str(self.bottom_right_y))
        QMessageBox.information(self, '좌표 설정 완료', f'우하단 좌표가 ({self.bottom_right_x}, {self.bottom_right_y})로 설정되었습니다.')
        print(f"x, y coordinates set to: ({self.bottom_right_x}, {self.bottom_right_y})")

    def run_screenshot_to_pdf(self):
        # 좌표 확인
        if (not self.left_x_input.text().strip() or not self.left_y_input.text().strip() or not self.right_x_input.text().strip() or not self.right_y_input.text().strip()):
            QMessageBox.warning(self, '입력 오류', '좌상단 및 우하단 좌표를 설정하세요.')
            return

        # 다음 페이지 버튼 설정 확인
        selected_button = self.radio_group.checkedButton()
        if selected_button is None:
            QMessageBox.warning(self, '입력 오류', '방향 버튼을 선택하세요.')
            return
        button_to_click = selected_button.text()

        # PDF 파일명 확인
        pdf_filename = self.pdf_input.text()
        if not pdf_filename:
            QMessageBox.warning(self, '입력 오류', 'PDF 파일명을 입력하세요.')
            return
        if not pdf_filename.endswith('.pdf'):
            pdf_filename += '.pdf'

        # 총 페이지 수 확인
        try:
            self.total_pages = int(self.total_pages_input.text())
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '유효한 총 페이지 수를 입력하세요.')
            return

        # 스크린샷 및 PDF 변환 실행
        self.current_page = 0
        self.take_screenshot_and_convert_to_pdf(self.left_x_input.text(), self.left_y_input.text(), self.right_x_input.text(), self.right_y_input.text(), button_to_click, pdf_filename)

    def take_screenshot_and_convert_to_pdf(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y, button, pdf_filename):
        # 카운트다운 시작
        for i in range(self.count_down, 0, -1):
            print(f"{i}초 후 스크린샷을 시작합니다.")
            time.sleep(1)

        screenshot_filenames = []

        # 지정된 좌표로 마우스 이동 및 클릭
        for page in range(self.total_pages):
            # 페이지 번호 증가
            self.current_page += 1

            # 스크린샷 파일명 설정
            screenshot_filename = f'image_{self.current_page}.png'

            # 좌표 값을 정수로 변환
            top_left_x = int(top_left_x)
            top_left_y = int(top_left_y)
            bottom_right_x = int(bottom_right_x)
            bottom_right_y = int(bottom_right_y)

            # 스크린샷 찍기
            screenshot_region = (top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y)
            screenshot = pyautogui.screenshot(region=screenshot_region)
            screenshot.save(screenshot_filename)

            screenshot_filenames.append(screenshot_filename)

            # 총 페이지 수에 도달하면 종료
            if self.current_page >= self.total_pages:
                break

            if button == '위':
                pyautogui.press('up')
            elif button == '아래':
                pyautogui.press('down')
            elif button == '왼쪽':
                pyautogui.press('left')
            elif button == '오른쪽':
                pyautogui.press('right')
            time.sleep(1)  # 딜레이

        # PDF로 변환
        self.convert_to_pdf(screenshot_filenames, pdf_filename)
        QMessageBox.information(self, '완료', f'{self.total_pages} 페이지가 완료되었습니다.')

    def convert_to_pdf(self, image_filenames, pdf_filename):
        pdf = canvas.Canvas(pdf_filename, pagesize=letter)
        for image_filename in image_filenames:
            image = Image.open(image_filename)
            pdf.drawImage(image_filename, 0, 0, width=letter[0], height=letter[1])
            pdf.showPage()
        pdf.save()
        QMessageBox.information(self, '완료', f'PDF 파일이 {pdf_filename}으로 저장되었습니다.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ConvertPdfApp()
    ex.show()
    sys.exit(app.exec_())
