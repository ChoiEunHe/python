import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class YouTubeController(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.driver = None

    def initUI(self):
        self.setWindowTitle('YouTube Controller')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Enter YouTube URL')
        layout.addWidget(self.url_input)

        self.load_button = QPushButton('Load Video', self)
        self.load_button.clicked.connect(self.load_video)
        layout.addWidget(self.load_button)

        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.play_video)
        layout.addWidget(self.play_button)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.pause_video)
        layout.addWidget(self.pause_button)

        self.forward_button = QPushButton('Forward 5s', self)
        self.forward_button.clicked.connect(self.forward_video)
        layout.addWidget(self.forward_button)

        self.backward_button = QPushButton('Backward 5s', self)
        self.backward_button.clicked.connect(self.backward_video)
        layout.addWidget(self.backward_button)

        self.web_view = QWebEngineView(self)
        layout.addWidget(self.web_view)

        self.setLayout(layout)

    def load_video(self):
        url = self.url_input.text()
        self.web_view.setUrl(QUrl(url))
        self.web_view.show()

        # Selenium driver 설정
        if self.driver is None:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
        self.driver.get(url)
        time.sleep(5)  # 영상 로드 대기

    def play_video(self):
        play_button = self.driver.find_element(By.CSS_SELECTOR, 'button.ytp-play-button')
        play_button.click()

    def pause_video(self):
        pause_button = self.driver.find_element(By.CSS_SELECTOR, 'button.ytp-play-button')
        pause_button.click()

    def forward_video(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)

    def backward_video(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_LEFT)

    def closeEvent(self, event):
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeController()
    ex.show()
    sys.exit(app.exec_())
