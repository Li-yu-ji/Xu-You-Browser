from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QUrl

class CustomWebPage(QWebEnginePage):
    def __init__(self, browser, parent=None):
        # 创建一个默认的 profile 如果没有提供
        profile = QWebEngineProfile.defaultProfile()
        super().__init__(profile, parent)
        self.browser = browser
        self.setup_settings()
        
    def setup_settings(self):
        """设置页面属性"""
        settings = self.settings()
        
        # 基本设置
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        
        # HTML5特性
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        
        # 增强HTML5媒体支持
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        
        # 添加更多HTML5媒体支持
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.SpatialNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, False)
        
        # 启用嵌入式播放器支持
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.XSSAuditingEnabled, False)
        
        # 启用更多HTML5功能
        settings.setAttribute(QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FocusOnNavigationEnabled, True)
        
        # 媒体编解码支持
        self.profile().setHttpAcceptLanguage("zh-CN,zh;q=0.9,en;q=0.8")
        self.profile().setHttpUserAgent(self.profile().httpUserAgent() + " HTML5Player/1.0")
        
        # 设置更多媒体相关属性
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        # 字体设置
        settings.setFontFamily(QWebEngineSettings.FontFamily.StandardFont, "Arial")
        settings.setFontSize(QWebEngineSettings.FontSize.DefaultFontSize, 16)
        
    def createWindow(self, _type):
        """处理新窗口请求"""
        try:
            new_page = CustomWebPage(self.browser, self)
            new_tab = self.browser.tab_manager.add_new_tab()
            new_tab.setPage(new_page)
            return new_page
        except Exception as e:
            print(f"创建新窗口失败: {e}")
            return None
        
    def javaScriptConsoleMessage(self, level, message, line, source):
        """处理JavaScript控制台消息"""
        print(f"JS Console ({source}:{line}): {message}")
        
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        """处理导航请求"""
        try:
            # 检测是否是媒体文件
            media_extensions = ['.mp4', '.webm', '.ogg', '.mp3', '.wav', '.m3u8', '.flv']
            if any(url.toString().lower().endswith(ext) for ext in media_extensions):
                # 如果是媒体文件，使用内置播放器打开
                self.browser.tab_manager.open_html5_player(url.toString())
                return False
            return super().acceptNavigationRequest(url, _type, isMainFrame)
        except Exception as e:
            print(f"处理导航请求失败: {e}")
            return True
            
    def certificateError(self, error):
        """处理证书错误"""
        # 允许所有证书，以支持更多视频网站
        return True 