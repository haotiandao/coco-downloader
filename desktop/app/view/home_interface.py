# coding: utf-8
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout

from qfluentwidgets import ScrollArea, isDarkTheme, setFont

from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..components import SearchCard, PlaceholderWidget, SongListWidget, SongInfo
from ..models.music import MusicItem
from ..services.music_search_service import search_music


class MusicSearchThread(QThread):
    """Search music without blocking the UI thread."""

    searchFinished = pyqtSignal(str, str, int, list)
    searchFailed = pyqtSignal(str, str, int, str)

    def __init__(self, keyword: str, platform: str, request_id: int, parent=None):
        super().__init__(parent)
        self.keyword = keyword
        self.platform = platform
        self.request_id = request_id

    def run(self):
        try:
            items = search_music(self.keyword, self.platform)
            self.searchFinished.emit(self.keyword, self.platform, self.request_id, items)
        except Exception as error:
            self.searchFailed.emit(
                self.keyword,
                self.platform,
                self.request_id,
                str(error),
            )


class HomeInterface(ScrollArea):
    """Home interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.searchCard = SearchCard(self)
        self.resultTitleLabel = QLabel(self)
        self.placeholderWidget = PlaceholderWidget(self)
        self.songListWidget = None
        self.searchThread = None
        self.searchRequestId = 0

        self._init_widget()
        self._connect_signals()

    def _init_widget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('homeInterface')

        self.scrollWidget.setObjectName('scrollWidget')
        self.resultTitleLabel.setObjectName('resultTitleLabel')
        self.resultTitleLabel.hide()
        setFont(self.resultTitleLabel, 28, QFont.Weight.Light)

        StyleSheet.HOME_INTERFACE.apply(self)
        self.scrollWidget.setStyleSheet("QWidget{background:transparent}")

        self._init_layout()

    def _init_layout(self):
        self.vBoxLayout.setSpacing(24)
        self.vBoxLayout.setContentsMargins(24, 10, 24, 10)

        self.vBoxLayout.addWidget(self.searchCard)
        self.vBoxLayout.addWidget(self.resultTitleLabel)
        self.vBoxLayout.addWidget(self.placeholderWidget, 1)

    def _connect_signals(self):
        self.searchCard.searchRequested.connect(self._on_search)

    def _on_search(self, keyword: str, platform: str):
        """Handle search request"""
        self.searchRequestId += 1
        request_id = self.searchRequestId
        self.placeholderWidget.hide()
        self.resultTitleLabel.setText(
            self.tr('"{keyword}" 的搜索结果').format(keyword=keyword)
        )
        self.resultTitleLabel.show()
        self.searchCard.setEnabled(False)
        self._show_placeholder(self.tr("正在搜索音乐"), self.tr("正在从 {platform} 获取结果...").format(platform=platform))

        thread = MusicSearchThread(keyword, platform, request_id, self)
        thread.searchFinished.connect(self._on_search_finished)
        thread.searchFailed.connect(self._on_search_failed)
        thread.finished.connect(thread.deleteLater)
        self.searchThread = thread
        thread.start()

    def _on_search_finished(
            self,
            keyword: str,
            platform: str,
            request_id: int,
            items: list[MusicItem],
    ):
        """Render search results"""
        if request_id != self.searchRequestId:
            return

        self.searchCard.setEnabled(True)
        if not items:
            self._clear_song_list()
            self._show_placeholder(
                self.tr("没有找到结果"),
                self.tr("平台 {platform} 没有返回可展示的歌曲").format(platform=platform),
            )
            return

        songs = [self._to_song_info(item) for item in items]
        self.placeholderWidget.hide()
        self._set_song_list(songs)

    def _on_search_failed(self, keyword: str, platform: str, request_id: int, message: str):
        """Render search failure state"""
        if request_id != self.searchRequestId:
            return

        self.searchCard.setEnabled(True)
        self._clear_song_list()
        self._show_placeholder(
            self.tr("搜索失败"),
            self.tr("{platform} 请求失败：{message}").format(
                platform=platform,
                message=message or self.tr("未知错误"),
            ),
        )

    def _set_song_list(self, songs: list[SongInfo]):
        """Create or update song list widget"""
        if self.songListWidget is None:
            self.songListWidget = SongListWidget(songs, self.scrollWidget)
            self.vBoxLayout.addWidget(self.songListWidget, 1)
        else:
            self.songListWidget.set_songs(songs)
            self.songListWidget.show()

    def _clear_song_list(self):
        """Hide previous search results"""
        if self.songListWidget is not None:
            self.songListWidget.hide()

    def _show_placeholder(self, title: str, description: str):
        """Show placeholder with custom text"""
        self.placeholderWidget.titleLabel.setText(title)
        self.placeholderWidget.descLabel.setText(description)
        self.placeholderWidget.show()

    def _to_song_info(self, item: MusicItem) -> SongInfo:
        """Convert provider item to list row data"""
        return SongInfo(
            title=item.title,
            singer=item.artist,
            album=item.album or self.tr("未知专辑"),
            duration=self._format_duration(item.duration),
        )

    def _format_duration(self, duration: str | None) -> str:
        """Format optional provider duration for display"""
        if not duration:
            return "--:--"
        if duration.startswith("00:") and len(duration.split(":")) == 3:
            return duration[3:]
        return duration
