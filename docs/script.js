const resultList = document.querySelector("#result-list");

function addField(container, label, value) {
  const group = document.createElement("dl");
  group.className = "result-field";
  const term = document.createElement("dt");
  term.textContent = label;
  const description = document.createElement("dd");
  description.textContent = value == null ? "未提供" : String(value);
  group.append(term, description);
  container.append(group);
}

async function showResults() {
  try {
    const response = await fetch("./results.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const report = await response.json();
    if (!Array.isArray(report.results)) throw new Error("JSON 缺少 results 陣列");

    document.querySelector("#model-name").textContent = report.model || "未提供";
    document.querySelector("#result-score").textContent = `${report.correct_count ?? "?"} / ${report.total ?? report.results.length}`;
    resultList.replaceChildren();

    for (const item of report.results) {
      const card = document.createElement("article");
      card.className = "result-card";
      const heading = document.createElement("div");
      heading.className = "result-heading";
      const title = document.createElement("h3");
      title.textContent = `測試編號：${item.id ?? "未知"}`;
      const status = document.createElement("span");
      status.className = `status ${item.category_correct === true ? "ok" : "bad"}`;
      status.textContent = item.category_correct === true ? "分類正確" : "分類不符";
      heading.append(title, status);
      card.append(heading);

      const prediction = item.prediction || {};
      addField(card, "輸入信件", item.input_email);
      addField(card, "預期分類", item.expected_category);
      addField(card, "實際分類", prediction.category);
      addField(card, "緊急程度", prediction.urgency);
      addField(card, "問題摘要", prediction.summary);
      addField(card, "建議回覆", prediction.suggested_reply);
      resultList.append(card);
    }
  } catch (error) {
    resultList.textContent = "無法讀取 results.json。請確認已執行 uv run batch_test.py，並使用本地 HTTP 伺服器開啟網站。";
    console.error("讀取測試結果失敗：", error);
    document.querySelector("#model-name").textContent = "讀取失敗";
    document.querySelector("#result-score").textContent = "—";
  }
}

showResults();
