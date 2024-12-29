from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, 
                           QTableWidgetItem, QHeaderView, QProgressBar)
from PyQt6.QtCore import Qt

class DownloadManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.downloads = {}
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("下载管理器")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        # 创建下载列表
        self.download_table = QTableWidget()
        self.download_table.setColumnCount(4)
        self.download_table.setHorizontalHeaderLabels(["文件名", "大小", "进度", "状态"])
        self.download_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.download_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        layout.addWidget(self.download_table)
        self.setLayout(layout)
        
    def handle_download(self, download):
        """处理下载请求"""
        try:
            self.add_download(download)
            download.accept()
            
            if not self.isVisible():
                self.show()
        except Exception as e:
            print(f"处理下载失败: {e}")
            
    def add_download(self, download):
        """添加下载项"""
        row = self.download_table.rowCount()
        self.download_table.insertRow(row)
        
        # 设置文件名
        filename = QTableWidgetItem(download.suggestedFileName())
        self.download_table.setItem(row, 0, filename)
        
        # 设置文件大小
        size = QTableWidgetItem("计算中...")
        self.download_table.setItem(row, 1, size)
        
        # 设置进度条
        progress = QProgressBar()
        self.download_table.setCellWidget(row, 2, progress)
        
        # 设置状态
        status = QTableWidgetItem("开始下载")
        self.download_table.setItem(row, 3, status)
        
        # 保存下载信息
        self.downloads[download] = {
            'row': row,
            'progress': progress
        }
        
        # 连接信号
        download.downloadProgress.connect(
            lambda received, total, d=download: self.update_progress(d, received, total))
        download.finished.connect(
            lambda d=download: self.download_finished(d))
            
    def update_progress(self, download, received, total):
        """更新下载进度"""
        if download in self.downloads:
            row = self.downloads[download]['row']
            progress = self.downloads[download]['progress']
            
            if total > 0:
                progress.setValue(int(received * 100 / total))
                self.download_table.item(row, 1).setText(self.format_size(total))
                
    def download_finished(self, download):
        """下载完成处理"""
        if download in self.downloads:
            row = self.downloads[download]['row']
            self.download_table.item(row, 3).setText("已完成")
            
    def format_size(self, size):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB" 