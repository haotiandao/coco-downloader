# coding: utf-8
from PyQt5.QtWidgets import QButtonGroup

from qfluentwidgets import BodyLabel, MessageBoxBase, RadioButton, SubtitleLabel

NETEASE_QUALITY_OPTIONS = [
    ("standard", "标准音质"),
    ("exhigh", "极高音质"),
    ("lossless", "无损音质"),
    ("hires", "Hi-Res 音质"),
    ("jyeffect", "高清环绕声"),
    ("sky", "沉浸环绕声"),
    ("jymaster", "超清母带"),
]


class NeteaseQualityDialog(MessageBoxBase):
    """Netease official download quality selector."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.selected_level = "lossless"
        self.button_group = QButtonGroup(self)
        self.title_label = SubtitleLabel(self.tr("选择下载音质"), self)
        self.desc_label = BodyLabel(self.tr("网易云官方接口支持多种音质，请选择本次下载使用的音质。"), self)

        self._init_widget()

    def _init_widget(self) -> None:
        self.yesButton.setText(self.tr("开始下载"))
        self.cancelButton.setText(self.tr("取消"))
        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.desc_label)

        for index, (level, label) in enumerate(NETEASE_QUALITY_OPTIONS):
            button = RadioButton(label, self)
            button.setProperty("level", level)
            button.setFixedHeight(32)
            self.button_group.addButton(button)
            self.viewLayout.addWidget(button)
            if level == self.selected_level:
                button.setChecked(True)

        self.button_group.buttonClicked.connect(self._on_button_clicked)

    def _on_button_clicked(self, button: RadioButton) -> None:
        level = button.property("level")
        if isinstance(level, str):
            self.selected_level = level
