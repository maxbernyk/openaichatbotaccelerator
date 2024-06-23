const documents = document.getElementById('documents');
const del_btn = document.getElementById('del_btn');
const upl_btn = document.getElementById('upl_btn');
const upl_menu = document.getElementById('upl_menu');
var selectedDoc = null;

del_btn.addEventListener("click", del_doc);
upl_btn.addEventListener("click", browse);

async function loadDocs() {
    documents.innerHTML = "loading...";
    const response = await fetch(
        "/admin",
        {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"action": "list"})
        }
    );
    const doc_list = await response.json();
    if (doc_list.length > 0) {
        htmlTable = ["<table>"];
        for (let i = 0; i < doc_list.length; i++) {
            htmlTable.push("<tr>");
            htmlTable.push("<td><input type=\"checkbox\" id=\"doc-" + doc_list[i]["id"] + "\" onclick=\"selectDoc(this);\"></td>");
            htmlTable.push("<td><a href=\"/doc?id=" + doc_list[i]["id"] + "\">" + doc_list[i]["filename"] + "</td>");
            htmlTable.push("<td class=\"doc-content\">" + doc_list[i]["content"] + "</td>");
            htmlTable.push("</tr>");
        }
        htmlTable.push("</table>");
        documents.innerHTML = htmlTable.join("");
        documents.style.visibility = "visible";
    } else {
        documents.style.visibility = "hidden";
    }
}

function del_doc() {
    if (selectedDoc != null) {
        var yes = confirm("Delete selected document?");
        if (yes) {
            documents.innerHTML = "deleting...";
                setTimeout(async function(){
                const response = await fetch(
                    "/admin",
                    {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({"action": "delete", "id": selectedDoc.id.replace("doc-", "")})
                    }
                );
                const answer = await response.text();
                loadDocs();
            }, 1)
        }
    }
}

function browse() {
    upl_menu.addEventListener("change", upload);
    upl_menu.click();
}

function upload() {
    documents.innerHTML = "uploading...";
    setTimeout(async function(){
        var data = new FormData();
        data.append('file', upl_menu.files[0]);
        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: data
            }
        );
        loadDocs();
    }, 1)
}

function selectDoc(doc) {
    if (doc.checked) {
        if (selectedDoc != null && selectedDoc != doc) {
            selectedDoc.checked = false;
        }
        selectedDoc = doc;
        del_btn.style.visibility = "visible";
    } else {
        selectedDoc = null;
        del_btn.style.visibility = "hidden";
    }
}

loadDocs();
