let currentCategory = "";
let currentQuestions = [];

const requirementInput = document.querySelector("#requirementInput");
const clarifyBtn = document.querySelector("#clarifyBtn");
const generateBtn = document.querySelector("#generateBtn");
const copyBtn = document.querySelector("#copyBtn");
const questionSection = document.querySelector("#questionSection");
const outputSection = document.querySelector("#outputSection");
const questionForm = document.querySelector("#questionForm");
const categoryBadge = document.querySelector("#categoryBadge");
const outputText = document.querySelector("#outputText");
const toast = document.querySelector("#toast");

function showToast(message) {
    toast.textContent = message;
    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("hidden");
    }, 2200);
}

function renderQuestions(questions) {
    questionForm.innerHTML = "";

    questions.forEach((item, index) => {
        const questionItem = document.createElement("div");
        questionItem.className = "question-item";

        const title = document.createElement("p");
        title.className = "question-title";
        title.textContent = `${index + 1}. ${item.question}`;
        questionItem.appendChild(title);

        const optionList = document.createElement("div");
        optionList.className = "option-list";

        item.options.forEach((option, optionIndex) => {
            const label = document.createElement("label");
            label.className = "option";

            const input = document.createElement("input");
            input.type = "radio";
            input.name = item.id;
            input.value = option;
            input.dataset.question = item.question;

            if (optionIndex === 0) {
                input.checked = true;
            }

            const text = document.createElement("span");
            text.textContent = option;

            label.appendChild(input);
            label.appendChild(text);
            optionList.appendChild(label);
        });

        questionItem.appendChild(optionList);
        questionForm.appendChild(questionItem);
    });
}

async function postJson(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    const result = await response.json();
    if (!response.ok) {
        throw new Error(result.error || "请求失败，请稍后再试。");
    }
    return result;
}

clarifyBtn.addEventListener("click", async () => {
    const requirement = requirementInput.value.trim();
    if (!requirement) {
        showToast("请先输入你的需求");
        return;
    }

    clarifyBtn.disabled = true;
    clarifyBtn.textContent = "正在生成选择题...";

    try {
        const result = await postJson("/api/clarify", { requirement });
        currentCategory = result.category;
        currentQuestions = result.questions;

        categoryBadge.textContent = currentCategory;
        renderQuestions(currentQuestions);
        questionSection.classList.remove("hidden");
        outputSection.classList.add("hidden");
    } catch (error) {
        showToast(error.message);
    } finally {
        clarifyBtn.disabled = false;
        clarifyBtn.textContent = "开始澄清需求";
    }
});

generateBtn.addEventListener("click", async () => {
    const requirement = requirementInput.value.trim();
    const checkedInputs = questionForm.querySelectorAll("input[type='radio']:checked");
    const answers = Array.from(checkedInputs).map((input) => ({
        question: input.dataset.question,
        answer: input.value,
    }));

    generateBtn.disabled = true;
    generateBtn.textContent = "正在调用 AI...";

    try {
        const result = await postJson("/api/generate", {
            requirement,
            category: currentCategory,
            answers,
        });

        const sourceText = result.model
            ? `生成方式：${result.source}（${result.model}）`
            : `生成方式：${result.source}`;
        const warningText = result.warning ? `\n提示：${result.warning}\n` : "";

        outputText.textContent = `${sourceText}${warningText}\n\n${result.prompt}`;
        outputSection.classList.remove("hidden");

        if (result.warning) {
            showToast(result.warning);
        }
    } catch (error) {
        showToast(error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "生成完整需求";
    }
});

copyBtn.addEventListener("click", async () => {
    const text = outputText.textContent.trim();
    if (!text) {
        showToast("没有可复制的内容");
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        showToast("已复制到剪贴板");
    } catch (error) {
        showToast("复制失败，请手动复制");
    }
});
