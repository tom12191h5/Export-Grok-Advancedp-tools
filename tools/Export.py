import requests
import json
import os
import time
import re

# ==============================
# type your cookie
# ==============================

cookies3 = ""

maxdata = 100

BASE = "https://grok.com/rest/app-chat"

headers = {
    "cookie": cookies3,
    "user-agent": "Mozilla/5.0",
    "accept": "*/*"
}


# ==============================
# 获取所有会话
# ==============================
def get_conversations():

    url = f"{BASE}/conversations?pageSize={maxdata}"

    r = requests.get(url, headers=headers)

    data = r.json()

    return data.get("conversations", [])


# ==============================
# 获取节点
# ==============================
def get_response_nodes(conversation_id):

    url = f"{BASE}/conversations/{conversation_id}/response-node?includeThreads=true"

    r = requests.get(url, headers=headers)

    data = r.json()

    return data.get("responseNodes", [])


# ==============================
# 加载聊天内容
# ==============================
def load_responses(conversation_id, response_ids):

    url = f"{BASE}/conversations/{conversation_id}/load-responses"

    payload = {
        "responseIds": response_ids
    }

    r = requests.post(url, headers=headers, json=payload)

    data = r.json()

    return data


# ==============================
# 导出 Markdown
# ==============================
def export_markdown(title, messages):

    safe = title.replace("/", "_")

    path = f"export/{safe}.md"

    with open(path, "w", encoding="utf-8") as f:

        f.write(f"# {title}\n\n")

        for m in messages:

            role = m.get("role")

            content = m.get("content", "")

            if role == "assistant":
                f.write("## Grok\n\n")
            else:
                f.write("## User\n\n")

            f.write(content)
            f.write("\n\n")


# ==============================
# 主程序
# ==============================
def main():

    os.makedirs("export", exist_ok=True)

    conversations = get_conversations()

    print("会话数量:", len(conversations))

    for c in conversations:

        cid = c["conversationId"]

        title = c.get("title", cid)

        print("抓取:", title)

        nodes = get_response_nodes(cid)

        response_ids = []

        for n in nodes:
            rid = n.get("responseId")
            if rid:
                response_ids.append(rid)

        if not response_ids:
            continue

        messages = load_responses(cid, response_ids)
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)

        with open(f"New5/{safe_title}.jsonl","w",encoding="UTF-8") as f:
            f.write(json.dumps(messages,indent=2,ensure_ascii=False))

        # export_markdown(title, messages)



if __name__ == "__main__":
    main()