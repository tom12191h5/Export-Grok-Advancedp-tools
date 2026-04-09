import sys
import json
import os
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QListWidget,
    QListWidgetItem
)

from PyQt5.QtWebEngineWidgets import QWebEngineView


def generate_html(data):

    responses = data.get("responses", [])

    html_messages = ""

    for r in responses:

        sender = r.get("sender", "")
        msg = r.get("message", "")
        time = r.get("createTime", "")

        try:
            t = datetime.fromisoformat(time.replace("Z", ""))
            time_str = t.strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = time

        cls = "human" if sender.lower() == "human" else "assistant"

        search_html = ""
        results = r.get("webSearchResults", [])

        if results:

            items = ""

            for s in results:

                url = s.get("url", "")
                title = s.get("title", "")
                preview = s.get("preview", "")

                items += f"""
                <li>
                <a href="{url}" target="_blank">{title}</a>
                <br>
                {preview}
                </li>
                """

            search_html = f"""
            <details class="search">
            <summary>搜索网页 ({len(results)})</summary>
            <ul>
            {items}
            </ul>
            </details>
            """

        html_messages += f"""
        <div class="message {cls}">
            <div class="meta">{sender} | {time_str}</div>
            <div class="bubble">{msg}</div>
            {search_html}
        </div>
        """

    html = f"""
    <html>

    <head>
    <meta charset="utf-8">

    <style>

    body {{
        font-family: Arial;
        background:#f5f5f5;
        padding:30px;
    }}

    .chat {{
        max-width:900px;
        margin:auto;
    }}

    .message {{
        margin:20px 0;
    }}

    .meta {{
        font-size:12px;
        color:#666;
        margin-bottom:5px;
    }}

    .bubble {{
        padding:15px;
        border-radius:10px;
        white-space:pre-wrap;
        line-height:1.6;
    }}

    .human .bubble {{
        background:#cfefff;
    }}

    .assistant .bubble {{
        background:#ffffff;
        border:1px solid #ddd;
    }}

    details {{
        margin-top:10px;
    }}

    </style>

    </head>

    <body>

    <div class="chat">

    <h2>Chat Viewer</h2>

    {html_messages}

    </div>

    </body>
    </html>
    """

    return html


class ChatViewer(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("JSONL Chat Viewer")

        self.resize(1400, 900)

        main_layout = QVBoxLayout()

        self.open_button = QPushButton("选择目录")

        main_layout.addWidget(self.open_button)

        body_layout = QHBoxLayout()

        self.list_widget = QListWidget()

        self.browser = QWebEngineView()

        body_layout.addWidget(self.list_widget, 1)
        body_layout.addWidget(self.browser, 4)

        main_layout.addLayout(body_layout)

        self.setLayout(main_layout)

        self.open_button.clicked.connect(self.open_directory)

        self.list_widget.itemClicked.connect(self.load_chat)

        self.file_map = {}


    def open_directory(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "选择目录"
        )

        if not folder:
            return

        self.list_widget.clear()
        self.file_map.clear()
        count = 0

        for root, dirs, files in os.walk(folder):

            for file in files:

                if file.endswith(".jsonl") or file.endswith(".json"):

                    path = os.path.join(root, file)

                    item = QListWidgetItem(file)

                    self.list_widget.addItem(item)
                    count +=1

                    self.file_map[file] = path
        print(count)


    def load_chat(self, item):

        file_name = item.text()

        path = self.file_map.get(file_name)

        if not path:
            return

        try:

            with open(path, "r", encoding="utf-8") as f:

                text = f.read().strip()

                if text.startswith("{"):

                    data = json.loads(text)

                else:

                    lines = text.splitlines()

                    data = json.loads(lines[0])

        except Exception as e:

            self.browser.setHtml(f"<h3>读取失败</h3><pre>{e}</pre>")

            return

        html = generate_html(data)

        self.browser.setHtml(html)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ChatViewer()

    window.show()

    sys.exit(app.exec_())