try:
    from PyQt6 import QtCore
    qt_version = 6
except ImportError:
    from PyQt5 import QtCore
    qt_version = 5

from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *

from . import utils


def settings_dialog():
    dialog = QDialog(mw)
    dialog.setWindowTitle("Anki Image Search v2 Addon")

    box_query = QHBoxLayout()
    label_query = QLabel("Query field:")
    text_query = QLineEdit("")
    text_query.setMinimumWidth(200)
    box_query.addWidget(label_query)
    box_query.addWidget(text_query)

    box_image = QHBoxLayout()
    label_image = QLabel("Image field:")
    text_image = QLineEdit("")
    text_image.setMinimumWidth(200)
    box_image.addWidget(label_image)
    box_image.addWidget(text_image)

    if qt_version == 5:
        ok = QDialogButtonBox(QDialogButtonBox.Ok)
        cancel = QDialogButtonBox(QDialogButtonBox.Cancel)
    else:
        ok = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        cancel = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)

    def init_configui():
        config = utils.get_config()
        text_query.setText(config["query_field"])
        text_image.setText(config["image_field"])

    def save_config():
        config = utils.get_config()
        config["query_field"] = text_query.text()
        config["image_field"] = text_image.text()
        mw.addonManager.writeConfig(__name__, config)

        dialog.close()

    def layout_everything():
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        layout.addLayout(box_query)
        layout.addLayout(box_image)

        layout.addWidget(ok)
        layout.addWidget(cancel)

    init_configui()
    ok.clicked.connect(save_config)
    cancel.clicked.connect(dialog.close)

    layout_everything()

    if qt_version == 5:
        dialog.exec_()
    else:
        dialog.exec()


def init_menu():
    action = QAction("Anki Image Search v2 settings", mw)
    qconnect(action.triggered, settings_dialog)
    mw.form.menuTools.addAction(action)
