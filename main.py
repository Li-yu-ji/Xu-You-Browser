from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QStandardPaths
import sys
import os

from ui.navigation import NavigationBar
from ui.tab_manager import TabManager
from managers.download_manager import DownloadManager

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 初始化配置
        self.init_profile()
        
        # 初始化UI和组件
        self.init_ui()
        
        # 初始化下载管理器
        self.download_manager = DownloadManager(self)
        
    def init_ui(self):
        """初始化UI"""
        # 设置窗口
        self.setWindowTitle('迅游浏览器')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建导航栏（先创建导航栏）
        self.navigation = NavigationBar(self)
        self.addToolBar(self.navigation)
        
        # 创建标签页管理器（后创建标签页）
        self.tab_manager = TabManager(self)
        self.setCentralWidget(self.tab_manager)
        
    def init_profile(self):
        """初始化浏览器配置"""
        self.profile = QWebEngineProfile("browser_profile")
        storage_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        
        # 设置存储路径
        self.profile.setPersistentStoragePath(os.path.join(storage_path, "browser_data"))
        self.profile.setCachePath(os.path.join(storage_path, "browser_cache"))
        
        # 配置基本设置
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        
        # Cookie设置
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        
        # 连接下载请求信号
        self.profile.downloadRequested.connect(lambda request: 
            self.download_manager.handle_download(request) if hasattr(self, 'download_manager') else None)

def main():
    try:
        app = QApplication(sys.argv)
        window = Browser()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"启动失败：{e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 