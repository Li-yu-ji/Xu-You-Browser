from PyQt6.QtWidgets import QToolBar, QPushButton, QLineEdit
from PyQt6.QtCore import QUrl

class NavigationBar(QToolBar):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.init_ui()
        
    def init_ui(self):
        """初始化导航栏UI"""
        self.setMovable(False)
        self.setup_buttons()
        self.setup_url_bar()
        self.setup_styles()
        
    def setup_buttons(self):
        """设置导航按钮"""
        # 延迟创建按钮回调
        def create_callback(func_name):
            def callback():
                if hasattr(self.browser, 'tab_manager'):
                    getattr(self.browser.tab_manager, func_name)()
            return callback
            
        def download_callback():
            if hasattr(self.browser, 'download_manager'):
                self.browser.download_manager.show()

        def player_callback():
            if hasattr(self.browser, 'tab_manager'):
                self.browser.tab_manager.open_html5_player()

        buttons = [
            ('←', create_callback('back'), '#2196F3'),
            ('→', create_callback('forward'), '#4CAF50'),
            ('⟳', create_callback('reload'), '#FF9800'),
            ('⌂', create_callback('navigate_home'), '#9C27B0'),
            ('+', create_callback('add_new_tab'), '#607D8B'),
            ('📂', create_callback('open_local_file'), '#E91E63'),
            ('↓', download_callback, '#795548'),
            ('▶', player_callback, '#FF5722'),
        ]
        
        for text, callback, color in buttons:
            btn = self.create_button(text, callback, color)
            self.addWidget(btn)
            
    def create_button(self, text, callback, color):
        """创建导航按钮"""
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setStyleSheet(self.get_button_style(color))
        return btn
        
    def setup_url_bar(self):
        """设置地址栏"""
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.addWidget(self.url_bar)
        
    def navigate_to_url(self):
        """导航到输入的URL"""
        if hasattr(self.browser, 'tab_manager'):
            url = self.url_bar.text()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            self.browser.tab_manager.load_url(QUrl(url))
        
    def update_url(self, url):
        """更新地址栏URL"""
        self.url_bar.setText(url.toString())
        
    def setup_styles(self):
        """设置样式"""
        self.setStyleSheet("""
            QToolBar {
                spacing: 5px;
                padding: 5px;
                background-color: #f8f9fa;
            }
        """)
        
        self.url_bar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 5px 10px;
                margin: 0 10px;
                font-size: 14px;
                min-width: 400px;
                height: 30px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        
    def get_button_style(self, color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                border-radius: 10px;
                min-width: 24px;
                min-height: 24px;
                padding: 2px 6px;
                color: white;
                font-weight: bold;
                font-size: 16px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 {color}, stop:1 {self.darken_color(color)});
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
        
    def darken_color(self, color):
        """使颜色变暗"""
        return color.replace('F', 'D').replace('E', 'C').replace('D', 'B') 