const userInputBox = document.getElementById('input_user');
const messagesContainer = document.getElementById('messages');
const buttonSend = document.getElementById('button_send');
const buttonNewConversation = document.getElementById('button_new_conversation');
const conversationListBox = document.getElementById('conversations');
const inputFile = document.getElementById('input_file');
const buttonContext = document.getElementById('button_context');

const currentConversation = {
    uuid: undefined, 
    statusFlag: false
};

const globalState = {
    viewingContext: false
};

function NewChatButton() {
    createNewChat();
    resetConversationLinkHighlights();
    messagesContainer.innerHTML = '';
    buttonContext.id = currentConversation.uuid;
    globalState.viewingContext = false;
}

buttonNewConversation.onclick = NewChatButton;

async function createNewChat(){
    const response = await fetch('/api/create');

    data = await response.json();

    if (response.ok) {
        currentConversation.uuid = data.uuid;
        currentConversation.statusFlag = true;
    }
}

buttonContext.onclick = async function(){
    if (currentConversation.uuid === undefined)
        return;

    if (globalState.viewingContext){
        loadCurrentConversationHistory();
        return;
    }

    messagesContainer.innerHTML = '';

    const response = await fetch('/api/context', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({
            uuid: currentConversation.uuid, 
        })
    })

    if (response.ok) {
        const history = await response.json();

        history.forEach(message => {
            addMessageBlob(message.role, message.content);
        });
    }

    globalState.viewingContext = true;
}

buttonSend.onclick = async function() {
    const userMessage = userInputBox.value;

    if (userMessage === '')
        return;

    if (currentConversation.uuid === undefined)
        return;

    let payLoad =  {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({
            model: null, 
            uuid: currentConversation.uuid, 
            messages: [
                {
                    role: 'user', 
                    content: [
                        {
                            type: 'text', 
                            text: userMessage
                        }
                    ]
                }
            ]
        })
    }

    if (inputFile.files.length > 0) {
        let body = JSON.parse(payLoad.body);
        body.messages[0].content.push({
            type: 'image_url', 
            image_url: {
                url: `data:${inputFile.files[0].type};base64,${await blobToBase64(inputFile.files[0])}`
            }
        });
        payLoad.body = JSON.stringify(body);
    }

    addMessageBlob('user', JSON.parse(payLoad.body).messages[0].content);
    userInputBox.value = '';
    inputFile.value = '';
    updateSendButtonState()

    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'message_box message_ai typing';
    typingIndicator.textContent = 'MikaGPT is thinking...';
    messagesContainer.appendChild(typingIndicator)
    scrollToBottom();

    const response = await fetch('/api/chat', payLoad)

    const reply = await response.json();
    addMessageBlob('assistant', reply);

    typingIndicator.remove();

    if (currentConversation.statusFlag) {
        await reLoadConversationList();
        document.getElementById(currentConversation.uuid).classList.add('active');
        currentConversation.statusFlag = false;
    }
}

function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.onerror = error => reject(error);
    });
}

function preProcessMarkdown(content) {
    // Escape only the necessary LaTeX-based markers that interfere with Markdown processing
    return content.replace(/((\\\[)|(\\\])|(\$\$))/g, (match) => {
        if (match === '\\[') return '\\\\\[';
        if (match === '\\]') return '\\\\\]';
        if (match === '$$') return '$$'; // Or handle '$$' differently if needed
        return match;
    });
}

function addMessageBlob(role, message) {
    if (role === 'system')
        return;

    const message_box = document.createElement('div');
    const buttonTTS = document.createElement('button');
    const image_box = document.createElement('img');

    // for backwards compatibility (since now message can be an array, and all the old messages were pure text)
    let text_message = null;
    if (message instanceof Array) {
        text_message = message[0].text;
        if (message.length > 1) {
            image_box.src = message[1].image_url.url;
        }
    }
    else
        text_message = message;

    buttonTTS.innerHTML = '🔊';
    buttonTTS.className = 'button_tts';
    buttonTTS.onclick = (event) => {
        const text = getReadableMessage(event.target.parentElement.innerHTML);
        playTTS(text);
    };

    // const display_role = role === 'user' ? 'YOU' : 'MikaGPT';
    const class_name = role === 'user' ? 'message_user' : 'message_ai';

    const marked_message = DOMPurify.sanitize(marked.parse(preProcessMarkdown(text_message)));

    message_box.className = `message_box ${class_name}`
    message_box.innerHTML += marked_message;

    message_box.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });

    message_box.appendChild(image_box);
    message_box.appendChild(buttonTTS);
    messagesContainer.appendChild(message_box);

    // renderMathInElement(message_box);
    MathJax.typeset([message_box]);
    scrollToBottom();
}

async function reLoadConversationList() {
    const response = await fetch('/api/convlist');
    data = await response.json();
    
    if (response.ok) {
        conversationListBox.innerHTML = '';

        let oldDateString = undefined;

        data.forEach(conversationInfo => {
            const dateString = formatEpochToDateString(conversationInfo.last_edited);

            if (oldDateString !== dateString) {
                const dateIndicator = document.createElement('div');
                dateIndicator.className = 'date_indicator';
                dateIndicator.innerHTML = dateString;
                conversationListBox.append(dateIndicator);
            }

            addConversationListElement(conversationInfo);

            oldDateString = dateString;
        });
    }
}

function formatEpochToDateString(epochTime) {
    const date = new Date(epochTime * 1000);
    
    const options = { month: 'short', day: 'numeric', year: 'numeric' };
    const month = date.toLocaleString('en-US', { month: 'short' });
    const day = date.getDate();
    const year = date.getFullYear();

    const suffix = (day) => {
        if (day > 3 && day < 21) return 'th';
        switch (day % 10) {
            case 1: return 'st';
            case 2: return 'nd';
            case 3: return 'rd';
            default: return 'th';
        }
    };

    return `${month}. ${day}${suffix(day)} ${year}`;
}

async function deleteConversation(uuid) {
    if (!confirm("Are you sure? This cannot be undone.")) {
        return;
    }

    console.log('deleting ' + uuid);

    const response = await fetch('/api/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({
            uuid: uuid, 
        })
    })

    console.log(response);
}

function addConversationListElement(conversation) {
    const link = document.createElement('a');
    link.href = '#';
    link.innerHTML = conversation.title === '' ? 'New Chat' : conversation.title;
    link.className = 'conversation_link';
    link.id = conversation.uuid;

    link.addEventListener('click', function(event) {
        if (currentConversation.uuid === event.target.id)
            return;

        resetConversationLinkHighlights();
        event.target.classList.add('active');
        currentConversation.uuid = conversation.uuid;
        currentConversation.statusFlag = false;
        loadCurrentConversationHistory();
    });

    const menuIcon = document.createElement('div');
    menuIcon.innerHTML = '⋮';
    menuIcon.className = 'button_chat_menu';
    menuIcon.onclick = function (event) {
        event.stopPropagation();
    }

    const dropMenu = document.createElement('div');
    dropMenu.className = 'drop_menu';
    dropMenu.onclick = function (event) {
        event.stopPropagation();
    }
    
    const buttonDelete = document.createElement('button');
    buttonDelete.className = 'button_delete_chat';
    buttonDelete.innerHTML = '🗑️';

    buttonDelete.onclick = function (event) {
        event.stopPropagation();
        deleteConversation(this.parentElement.parentElement.parentElement.id);
        reLoadConversationList();
        NewChatButton();
    }

    dropMenu.appendChild(buttonDelete);
    menuIcon.appendChild(dropMenu);
    link.appendChild(menuIcon);

    conversationListBox.appendChild(link);
}

function resetConversationLinkHighlights() {
    const conversationLinks = document.getElementsByClassName('conversation_link');
    [].forEach.call(conversationLinks, link => {
        link.classList.remove('active');
    });
}

async function loadCurrentConversationHistory() {
    if (currentConversation.uuid === undefined)
        return;

    messagesContainer.innerHTML = '';

    const response = await fetch('/api/history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({
            uuid: currentConversation.uuid, 
        })
    })

    if (response.ok) {
        const history = await response.json();

        history.forEach(message => {
            addMessageBlob(message.role, message.content);
        });
    }

    buttonContext.id = currentConversation.uuid;
    globalState.viewingContext = false;
}

async function playTTS(text) {
    const response = await fetch('/api/tts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }, 
        body: JSON.stringify({
            text: text, 
        })
    });

    if (response.ok) {
        const blob = await response.blob();
        const audioURL = URL.createObjectURL(blob);
        const audio = new Audio(audioURL);
        
        audio.play();
        audio.onended = () => URL.revokeObjectURL(audioURL);
    }
}

function getReadableMessage(target) {
    const tempDiv = document.createElement('div');
    
    tempDiv.innerHTML = target;
    tempDiv.querySelectorAll(['pre', 'button']).forEach(codeBlock => codeBlock.remove());

    return tempDiv.textContent || tempDiv.innerText || '';
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateSendButtonState() {
    buttonSend.disabled = userInputBox.value.trim() === '';
}

document.addEventListener('DOMContentLoaded', function() {
    reLoadConversationList();
    createNewChat();
});

userInputBox.addEventListener('input', updateSendButtonState);