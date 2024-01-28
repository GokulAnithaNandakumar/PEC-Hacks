
const messageForm = document.getElementById("messageForm");
const messageInput = document.getElementById("message");
const chatHistory = document.getElementById("chat-history");
const responseElement = document.getElementById("response");
let userActive = "";

let setUser= (x) =>{
    user = x;

}
messageForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const userMessage = messageInput.value;
    appendMessage("Helper", userMessage);
    sendReply();
    messageInput.value = "";
});

function loadUserList() {
    fetch("/get_users/")
        .then(response => response.json())
        .then(data => {
            const userListContainer = document.getElementById("user-list-container");
            userListContainer.innerHTML = "";
            data.users.forEach(user => {
                const userElement = document.createElement("p");
                userElement.textContent = user;
                userElement.classList.add("user-list-item");
                userElement.addEventListener("click", () => {loadChatHistoryForUser(user);setUser(user);});
                userListContainer.appendChild(userElement);
            });
        })
        .catch(error => {
            console.error("Error loading user list:", error);
        });
}

function loadChatHistoryForUser(user) {
    // Fetch and display chat history for the selected user
    fetch(`/get_chat_history_for_user/?user=${user}`)
        .then(response => response.json())
        .then(data => {
            const serverChatHistory = data.chat_history;
            chatHistory.innerHTML = "";
            serverChatHistory.forEach(entry => {
                const { type, content } = entry;
                if (type === 'message') {
                    appendMessage("User", content);
                } else if (type === 'reply') {
                    appendMessage("Helper", content);
                }
            });
        })
        .catch(error => {
            console.error("Error loading chat history:", error);
        });
}

loadUserList();
setInterval(loadUserList, 5000);
loadChatHistoryFromFirebase();
setInterval(loadChatHistoryForUser(userActive), 5000);
function loadChatHistoryFromFirebase() {
    fetch("/get_chat_history/")
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch chat history: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const serverChatHistory = data.chat_history;  // Rename this variable to avoid confusion

            // Clear the existing chat history in the DOM
            chatHistory.innerHTML = "";

            // Iterate through the chat history received from the server and append messages or replies
            serverChatHistory.forEach(entry => {
                const { type, content } = entry;
                if (type === 'message') {
                    appendMessage("User", content); // Use the user's name here
                } else if (type === 'reply') {
                    appendMessage("Helper", content);
                }
            });
        })
        .catch(error => {
            console.error("Error loading chat history:", error);
        });
}

function getUserMessage() {
    return messageInput.value;
}

function sendReply() {
    const message = getUserMessage();
    fetch("/send_reply/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({user:userActive, message: message }),
    })
        .then((response) => {
            if (response.status === 202) {
                console.log("Message sent to the backend");
            }
        })
        .catch((error) => {
            console.log(error);
        });
}


function getCSRFToken() {
    const csrfCookie = document.cookie
        .split("; ")
        .find((cookie) => cookie.startsWith("csrftoken="));
    return csrfCookie ? csrfCookie.split("=")[1] : "";
}



function appendMessage(sender, message) {
    const messageElement = document.createElement('p');

    if (sender === 'User') {
        messageElement.className = 'user-message';
    } else if (sender === 'Helper') {
        messageElement.className = 'bot-message';
    } else if (sender === "Err") {
        sender = 'Error Bot';
        messageElement.className = 'err-message';
    }

    messageElement.innerHTML = `<strong>${sender} : </strong> ${message}`;
    chatHistory.appendChild(messageElement);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}