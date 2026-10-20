
from pathlib import Path
from typing import Literal
import json

from ollama import chat
from pydantic import BaseModel


# ==========================================
# 1. 模型設定
# ==========================================
MODEL_NAME = "qwen2.5:3b"


# ==========================================
# 2. 定義 AI 結構化輸出格式
# ==========================================
class EmailResult(BaseModel):
    category: Literal[
        "物流問題", "退款問題", "產品問題", "其他"
    ]
    urgency: Literal["高", "中", "低"]
    summary: str
    suggested_reply: str


# ==========================================
# 3. 輸入測試信件
# ==========================================
email_text = """
您好，我收到耳機後發現左耳完全沒有聲音，想請問可以怎麼處理？
"""


# ==========================================
# 4. 呼叫 LLM 並分類
# ==========================================
def classify_email(email: str) -> EmailResult:

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位專業的客服信件分類助手。"
                    "請使用繁體中文回答。"
                    "將信件分類為物流問題、退款問題、"
                    "產品問題或其他。"
                    "判斷緊急程度為高、中、低。"
                    "提供簡短的問題摘要及禮貌的建議回覆。"
                    "不得編造訂單狀態或客戶資訊。"
                ),
            },
            {
                "role": "user",
                "content": email,
            },
        ],
        format=EmailResult.model_json_schema(),
        options={"temperature": 0},
    )

    result = EmailResult.model_validate_json(
        response.message.content
    )

    return result


# ==========================================
# 5. 執行與儲存結果
# ==========================================
def main():

    print("AI 客服信件分類器")
    print("正在呼叫 Ollama，請稍候...\n")

    result = classify_email(email_text)

    output = {
        "model": MODEL_NAME,
        "input_email": email_text.strip(),
        "classification": result.model_dump(),
    }

    json_text = json.dumps(
        output,
        ensure_ascii=False,
        indent=2,
    )

    print(json_text)

    # 儲存結果，供後續 GitHub Pages 使用
    output_path = Path("docs/result.json")
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        json_text,
        encoding="utf-8"
    )

    print(f"\n完成！結果已儲存：{output_path}")


if __name__ == "__main__":
    main()
