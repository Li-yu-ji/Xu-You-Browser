from PyQt6.QtWidgets import QTabWidget, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from web.custom_page import CustomWebPage

class TabManager(QTabWidget):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.tab_changed)
        self.add_new_tab()

    def add_new_tab(self, url=None):
        """添加新标签页"""
        web_view = QWebEngineView()
        web_page = CustomWebPage(self.browser, web_view)
        web_view.setPage(web_page)
        
        # 连接信号 - 使用延迟连接
        def update_url(url):
            if hasattr(self.browser, 'navigation'):
                self.browser.navigation.update_url(url)
            
        web_view.urlChanged.connect(update_url)
        web_view.titleChanged.connect(lambda title: self.update_tab_title(web_view, title))
        
        # 设置初始URL
        if url:
            web_view.setUrl(QUrl(url))
        else:
            web_view.setUrl(QUrl("about:blank"))
            
        # 添加标签页
        index = self.addTab(web_view, "新标签页")
        self.setCurrentIndex(index)
        return web_view

    def update_tab_title(self, web_view, title):
        """更新标签页标题"""
        index = self.indexOf(web_view)
        if index != -1:
            self.setTabText(index, title)

    def close_tab(self, index):
        """关闭标签页"""
        if self.count() > 1:
            self.removeTab(index)
        else:
            self.currentWidget().setUrl(QUrl("about:blank"))

    def tab_changed(self, index):
        """标签页切换时更新URL"""
        if index != -1 and hasattr(self.browser, 'navigation'):
            url = self.currentWidget().url()
            self.browser.navigation.update_url(url)

    def load_url(self, url):
        """加载URL"""
        if isinstance(url, str):
            url = QUrl(url)
        if not url.scheme():
            # 如果URL没有协议，尝试添加http://
            url = QUrl("http://" + url.toString())
        self.currentWidget().setUrl(url)

    def back(self):
        """后退"""
        if self.currentWidget():
            self.currentWidget().back()

    def forward(self):
        """前进"""
        if self.currentWidget():
            self.currentWidget().forward()

    def reload(self):
        """刷新"""
        if self.currentWidget():
            self.currentWidget().reload()

    def navigate_home(self):
        """导航到主页"""
        self.load_url(QUrl("about:blank"))

    def open_local_file(self):
        """打开本地文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "打开文件", 
            "", 
            "HTML Files (*.html);;All Files (*.*)"
        )
        if file_path:
            self.load_url(QUrl.fromLocalFile(file_path)) 

    def open_html5_player(self, media_url=None):
        """打开HTML5播放器"""
        try:
            player_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>HTML5 播放器</title>
                <meta charset="utf-8">
                <style>
                    body {
                        margin: 0;
                        padding: 20px;
                        background: #f0f0f0;
                        font-family: Arial, sans-serif;
                    }
                    .player-container {
                        max-width: 800px;
                        margin: 0 auto;
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    .video-container {
                        width: 100%;
                        margin-bottom: 20px;
                        position: relative;
                        padding-top: 56.25%;
                    }
                    video {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        border-radius: 5px;
                        background: #000;
                    }
                    .controls {
                        margin-top: 20px;
                    }
                    input[type="file"], input[type="text"] {
                        display: block;
                        margin: 10px 0;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        width: 100%;
                        box-sizing: border-box;
                    }
                    h2 {
                        color: #333;
                        margin-bottom: 20px;
                    }
                    .error-message {
                        color: red;
                        margin: 10px 0;
                        display: none;
                    }
                    .format-support {
                        margin-top: 10px;
                        color: #666;
                        font-size: 0.9em;
                    }
                </style>
            </head>
            <body>
                <div class="player-container">
                    <h2>HTML5 媒体播放器</h2>
                    <div class="video-container">
                        <video id="player" controls crossorigin="anonymous" preload="auto">
                            您的浏览器不支持 HTML5 视频播放。
                        </video>
                    </div>
                    <div class="error-message" id="errorMessage"></div>
                    <div class="controls">
                        <input type="text" id="urlInput" class="url-input" 
                               placeholder="输入媒体URL或拖放文件到此处">
                        <input type="file" id="fileInput" accept="video/*,audio/*">
                        <div class="format-support">
                            支持格式: MP4, WebM, OGG, MP3, WAV, M3U8
                        </div>
                    </div>
                </div>
                <script>
                    const player = document.getElementById('player');
                    const fileInput = document.getElementById('fileInput');
                    const urlInput = document.getElementById('urlInput');
                    const errorMessage = document.getElementById('errorMessage');
                    
                    // 错误处理
                    player.addEventListener('error', function(e) {
                        console.error('播放错误:', e);
                        errorMessage.style.display = 'block';
                        errorMessage.textContent = '播放出错: ' + (player.error ? player.error.message : '未知错误');
                    });
                    
                    // 处理文件选择
                    fileInput.addEventListener('change', function(e) {
                        try {
                            const file = e.target.files[0];
                            if (file) {
                                const url = URL.createObjectURL(file);
                                player.src = url;
                                urlInput.value = file.name;
                                player.play().catch(console.error);
                            }
                        } catch(err) {
                            console.error('文件处理错误:', err);
                            errorMessage.style.display = 'block';
                            errorMessage.textContent = '文件处理错误: ' + err.message;
                        }
                    });
                    
                    // 处理URL输入
                    urlInput.addEventListener('change', function(e) {
                        try {
                            const url = e.target.value.trim();
                            if (url) {
                                player.src = url;
                                player.play().catch(console.error);
                            }
                        } catch(err) {
                            console.error('URL处理错误:', err);
                            errorMessage.style.display = 'block';
                            errorMessage.textContent = 'URL处理错误: ' + err.message;
                        }
                    });
                    
                    // 处理拖放
                    document.addEventListener('dragover', function(e) {
                        e.preventDefault();
                    });
                    
                    document.addEventListener('drop', function(e) {
                        e.preventDefault();
                        try {
                            const file = e.dataTransfer.files[0];
                            if (file) {
                                const url = URL.createObjectURL(file);
                                player.src = url;
                                urlInput.value = file.name;
                                player.play().catch(console.error);
                            }
                        } catch(err) {
                            console.error('拖放处理错误:', err);
                            errorMessage.style.display = 'block';
                            errorMessage.textContent = '拖放处理错误: ' + err.message;
                        }
                    });
                    
                    // 设置初始媒体URL（如果有）
                    if ('%s') {
                        try {
                            player.src = '%s';
                            urlInput.value = '%s';
                            player.play().catch(console.error);
                        } catch(err) {
                            console.error('初始化错误:', err);
                            errorMessage.style.display = 'block';
                            errorMessage.textContent = '初始化错误: ' + err.message;
                        }
                    }
                </script>
            </body>
            </html>
            """ % (media_url or '', media_url or '', media_url or '')
            
            # 创建新标签页并加载播放器
            web_view = self.add_new_tab()
            web_view.setHtml(player_html)
            return web_view
            
        except Exception as e:
            print(f"打开播放器失败: {e}")
            return None 