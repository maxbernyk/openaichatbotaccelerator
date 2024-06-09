const prompt = document.getElementById('prompt');
const button = document.getElementById('button');
const history = document.getElementById('history');

button.addEventListener("click", ask);

if (!history.innerHTML || history.innerHTML.trim() === "") {
    history.style.visibility = "hidden";
}

async function ask() {
    if (history.style.visibility == "hidden") {
        history.style.visibility = "visible";
    }
    q = prompt.value;
    prompt.value = "";
    history_html = history.innerHTML;
    history.innerHTML = history_html + "<div class=\"msg-sent\">" + q + "</div>" + "<div class=\"msg-rcvd\">...</div>";
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
