const prompt = document.getElementById('prompt');
const button = document.getElementById('button');
const history = document.getElementById('history');
const btn_clear = document.getElementById('btn_clear');
const rememberHistory = document.getElementById('rememberHistory');

button.addEventListener("click", ask);
prompt.addEventListener("keypress", onKeypress);
btn_clear.addEventListener("click", clearChat);

if (!history.innerHTML || history.innerHTML.trim() === "") {
    history.style.visibility = "hidden";
}

async function ask() {
    q = prompt.value;
    prompt.value = "";
    if (!rememberHistory.checked) {
        clearChat();
    }
    if (history.style.visibility == "hidden") {
        history.style.visibility = "visible";
    }
    history_html = history.innerHTML;
    history.innerHTML = history_html + "<div class=\"msg-sent\">" + q + "</div>" + "<div class=\"msg-rcvd\">...</div>";
    history.scrollTop = history.scrollHeight;
    const response = await fetch(
        "/prompt",
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"q": q})
        }
    );
    const answer = await response.text();
    history.innerHTML = history_html + "<div class=\"msg-sent\">" + q + "</div>" + "<div class=\"msg-rcvd\">" + answer + "</div>";
    history.scrollTop = history.scrollHeight;
}

async function clearChat() {
    history.innerHTML = "";
    history.style.visibility = "hidden";
    const response = await fetch(
        "/clear",
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"action": "clear"})
        }
    );
    const answer = await response.text();
}

function onKeypress(e) {
    if (e.keyCode === 13 && !e.shiftKey) {
        e.preventDefault();
        ask();
    }
}
