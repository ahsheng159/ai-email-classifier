
import json
from pathlib import Path

from main import classify_email, MODEL_NAME

# 專案根目錄
BASE_DIR = Path(__file__).resolve().parent

# 測試資料
INPUT_FILE = BASE_DIR / "examples" / "test_cases.json"

# 輸出結果
OUTPUT_FILE = BASE_DIR / "docs" / "results.json"


def main():
    # 讀取三封測試信件
    cases = json.loads(
        INPUT_FILE.read_text(encoding="utf-8")
    )

    results = []

    for case in cases:
        print(f"正在分析：{case['id']}")

        # 呼叫之前完成的 LLM 分類函式
        prediction = classify_email(case["email"])

        # 比較 AI 分類與預期分類
        correct = (
            prediction.category == case["expected_category"]
        )

        results.append({
            "id": case["id"],
            "input_email": case["email"],
            "expected_category": case["expected_category"],
            "prediction": prediction.model_dump(),
            "category_correct": correct,
        })

        print(f"預期：{case['expected_category']}")
        print(f"實際：{prediction.category}")
        print(f"分類正確：{correct}\n")

    # 統計分類正確筆數
    correct_count = sum(
        item["category_correct"] for item in results
    )

    report = {
        "model": MODEL_NAME,
        "total": len(results),
        "correct_count": correct_count,
        "note": "僅自動檢查分類類別，其他文字輸出需人工審核。",
        "results": results,
    }

    # 儲存全部結果
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_FILE.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8",
    )

    print("========================")
    print(f"總測試數：{len(results)}")
    print(f"分類正確：{correct_count}")
    print(f"結果檔案：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
