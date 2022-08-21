from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *

def settings_dialog():
    dialog = QDialog(mw)
    dialog.setWindowTitle("Anki Image Search v2 Addon")

    box_query = QHBoxLayout()
    label_query = QLabel("Query field:")
    text_query = QLineEdit("")
    text_query.setMinimumWidth(100)
    box_query.addWidget(label_query)
    box_query.addWidget(text_query)
    
    box_image = QHBoxLayout()
    label_image = QLabel("Image field:")
    text_image = QLineEdit("")
    text_image.setMinimumWidth(100)
    box_image.addWidget(label_image)
    box_image.addWidget(text_image)

    ok = QDialogButtonBox(QDialogButtonBox.Ok)
    cancel = QDialogButtonBox(QDialogButtonBox.Cancel)

    def init_configui():
        config = mw.addonManager.getConfig(__name__)
        text_query.setText(config["query_field"])
        text_image.setText(config["image_field"])

    def confirm_config():
        config = mw.addonManager.getConfig(__name__)
        config["image_field"] = text_query.text()
        config["query_field"] = text_image.text()
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
    ok.clicked.connect(confirm_config)
    cancel.clicked.connect(dialog.close)

    layout_everything()

    dialog.exec_()


def init_menu():
    action = QAction("Anki Image Search v2 settings", mw)
    qconnect(action.triggered, settings_dialog)
    mw.form.menuTools.addAction(action)
