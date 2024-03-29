//定义全局变量
const input = document.getElementById('input');
const output = document.getElementById('output');
const ocrBtn = document.getElementById('ocrBtn');
const chatBtn = document.getElementById('chatBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');


//主题颜色方法-点击按钮改变输入输出的边框颜色
const inputBox = document.getElementById("input");
const imgBox = document.getElementById("image-container");
const outputBox = document.getElementById("output");

function scrollToBottom() {
    const chatBox = document.getElementById("chat-content");
    chatBox.scrollTop = chatBox.scrollHeight - chatBox.clientHeight;
}

const confirmBox = document.getElementById('confirmBox');
const yesBtn = document.getElementById('yesBtn');
const noBtn = document.getElementById('noBtn');

document.addEventListener('click', (e) => {
    if (e.target !== clearBtn && e.target !== confirmBox && confirmBox.classList.contains('show')) {
        confirmBox.classList.remove('show');
    }
});

document.getElementById('chat-content').addEventListener('click', (event) => {
    if (event.target.matches('.copy-code')) {
        const preElement = event.target.parentElement.previousElementSibling;
        const codeElement = preElement.querySelector('code');
        const codeText = codeElement.textContent;
        const textArea = document.createElement('textarea');
        textArea.value = codeText;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('Copy');
        textArea.remove();

        layer.msg('复制成功!', {
            time: 500, // 设置显示时间，单位为毫秒
            offset: '100px', // 设置距离顶部的距离
            icon: 1,
        });
    }
});
const md = new window.markdownit({
    html: true,
    linkify: true,
    typographer: true,
    highlight: function (str, lang) {
        if (lang && hljs.getLanguage(lang)) {
            try {
                return hljs.highlight(lang, str).value;
            } catch (__) {
            }
        }

        try {
            return hljs.highlightAuto(str).value;
        } catch (__) {
        }

        return ''; // 使用默认的转义
    },
});

const defaultRender = md.renderer.rules;

// 自定义渲染规则
md.renderer.rules = {
    ...defaultRender,
    code_block: (tokens, idx, options, env, self) => {
        const token = tokens[idx];
        const code = md.utils.escapeHtml(token.content);
        return `<pre>
          <code>${code}</code>
          <div class="copy-code-wrapper">
          <span>
          <span class="copy-code">复制代码</span>
          </span>
          </div>
          </pre>`;
    },
    heading_open: () => '<p>',
    heading_close: () => '</p>',


};
md.renderer.rules.ordered_list_open = (tokens, idx) => {
    const attrs = tokens[idx].attrs;
    const start = attrs ? attrs.find(([name]) => name === 'start') : null;
    const startAttr = start ? ` start="${start[1]}"` : '';
    const orderType = start ? ` type="${start[1] > 9 ? '1' : 'a'}"` : '';
    return `<ol class="my-ordered-list"${startAttr}${orderType}>`;
};


md.renderer.rules.ordered_list_close = (tokens, idx) => {
    return `</ol>`;
};

md.renderer.rules.list_item_open = (tokens, idx) => {
    return `<li class="my-list-item">`;
};

md.renderer.rules.list_item_close = (tokens, idx) => {
    return `</li>`;
};

md.renderer.rules.bullet_list_open = (tokens, idx) => {
    return `<ul class="my-bullet-list">`;
};

md.renderer.rules.bullet_list_close = (tokens, idx) => {
    return `</ul>`;
};


let isTyping = false;
const host = window.location.hostname;
const port = window.location.port;
let url = `ws://${host}:${port}/tool/chat`;
if (host === 'chat250.top') {
    url = `wss://${host}/tool/chat`;

}

let socket = null;
let retryCount = 0; // 记录重连次数
let isReconnecting = false; // 标记是否正在重连
let accumulatedText = '';

function resetAccumulatedText() {
    accumulatedText = '';
}

function connect() {
    socket = new WebSocket(url);

    socket.addEventListener('open', (event) => {
        console.log('WebSocket connected:', event);
        retryCount = 0; // 连接成功，将重连次数归零
        isReconnecting = false; // 连接成功，将重连状态重置
    });


    socket.addEventListener('message', (event) => {
        saveChatContent()
        const receivedData = JSON.parse(event.data);
        if (receivedData.lastmsg3list) {
            savelastmsg3list(receivedData.lastmsg3list)
            isTyping = false;
        }
        if (receivedData.lastmsg5list) {
            savelastmsg5list(receivedData.lastmsg5list)
            isTyping = false;
        }
        if (receivedData.lastmsg6list) {
            savelastmsg6list(receivedData.lastmsg6list)
            isTyping = false;
        }
        if (receivedData.lastmsg7list) {
            savelastmsg7list(receivedData.lastmsg7list)
            isTyping = false;
        }
        if (receivedData.lastmsg8list) {
            isTyping = false;
        }
        if (receivedData.lastmsg9list) {
            savelastmsg9list(receivedData.lastmsg9list)
            isTyping = false;
        }
        if (receivedData.lastmsg12list) {
            savelastmsg12list(receivedData.lastmsg12list)
            isTyping = false;
        }
        if (receivedData.lastmsg14list) {
            savelastmsg14list(receivedData.lastmsg14list)
            isTyping = false;
        }
        if (receivedData.lastmsg15list) {
            savelastmsg15list(receivedData.lastmsg15list)
            isTyping = false;
        }

        const replyElement = document.getElementById('temporary-reply').querySelector('.message');
        const blinkElement = replyElement.querySelector('.placeholder-cursor');
        const chatContent = document.getElementById('chat-content');
        const userInput = document.getElementById('messageInput');

        // 创建一个监听 element 内容更改的 MutationObserver
        const observer = new MutationObserver(() => {
            chatContent.scrollTop = chatContent.scrollHeight;
        });

        // 开始监听 element 的子节点变化
        observer.observe(replyElement, {childList: true, subtree: true});
        if (receivedData.text && receivedData.text !== 'THE_END_哈哈哈') {
            isTyping = true;
            replyElement.style.whiteSpace = 'pre-line';

            // 将新的 receivedData.text 添加到累积的文本中
            accumulatedText += receivedData.text;


            const renderedHtml = md.render(accumulatedText);
            replyElement.innerHTML = addCopyCodeButtons(renderedHtml);


            chatContent.scrollTop = chatContent.scrollHeight;
            if (!isMobileDevice()) {
              userInput.focus();
            }

            if (receivedData.id) {
                saveid(receivedData.id)
            }
            if (receivedData.miniid) {
                saveminiid(receivedData.miniid)
            }
            if (receivedData.id360) {
                saveid360(receivedData.id360)
            }

            // 停止监听 element 的子节点变化
            observer.disconnect();

        } else if (receivedData.text && receivedData.text === 'THE_END_哈哈哈') {
            isTyping = false;
            chatContent.scrollTop = chatContent.scrollHeight;
            if (!isMobileDevice()) {
              userInput.focus();
            }
            // 停止监听 element 的子节点变化
            observer.disconnect();
        }
        saveChatContent();
        linksblank()
    });


    socket.addEventListener('close', (event) => {
        console.log('WebSocket closed:', event);
        if (!isReconnecting) {
            isReconnecting = true;
            const retryInterval = Math.min(30, Math.pow(2, retryCount)) * 1000; // 计算重连间隔，不超过 30 秒

            // 显示“异常断开，请重新键入”信息
            const replyElement = document.getElementById('temporary-reply').querySelector('.message');
            const blinkElement = replyElement.querySelector('.placeholder-cursor');
            const chatContent = document.getElementById('chat-content');
            const userInput = document.getElementById('messageInput');

            replyElement.style.whiteSpace = 'pre-line';

            replyElement.innerHTML = '连接异常，请尝试更换通道或者联系管理员试试吧！';


            chatContent.scrollTop = chatContent.scrollHeight;
            blinkElement.classList.remove('blink'); // 去除闪烁光标
            if (!isMobileDevice()) {
              userInput.focus();
            }



            setTimeout(connect, retryInterval); // 定时器中执行重连
            retryCount++; // 增加重连次数
        }
        isTyping = false;
    });


    socket.addEventListener('error', (event) => {
        console.error('WebSocket error:', event);
    });
}

// 初始化连接
connect();
// 定时检查WebSocket状态并尝试重连
let reconnectCount = 0; // 记录已尝试的重连次数
const maxReconnectCount = 10; // 最大重连次数

const checkAndReconnect = () => {
    if (!socket || socket.readyState === WebSocket.CLOSED) {
        if (reconnectCount >= maxReconnectCount) {
            console.log(`WebSocket尝试重连${maxReconnectCount}次仍失败，已停止尝试`);
            clearInterval(intervalID); // 清除定时器
            return;
        }
        connect();
        loadChatContent();
        reconnectCount++;
    } else {
        reconnectCount = 0; // 已连接，重置重连次数
    }
};

// 设置定时器以检查并重连WebSocket（每隔10秒）
const intervalID = setInterval(checkAndReconnect, 10000);

function addCopyCodeButtons(htmlString) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlString, 'text/html');
    const preElements = doc.querySelectorAll('pre');

    preElements.forEach((pre) => {
        const copyCodeWrapper = document.createElement('div');
        copyCodeWrapper.className = 'copy-code-wrapper';

        const copyCodeSpan = document.createElement('span');
        copyCodeSpan.className = 'copy-code';
        copyCodeSpan.textContent = '复制代码';

        copyCodeWrapper.appendChild(copyCodeSpan);

        // 将 pre 元素包裹在一个 div 中，并将该 div 作为父元素
        const parentDiv = document.createElement('div');
        parentDiv.style.position = 'relative';  // 给父元素加上相对定位

        // 插入新创建的 div 到 pre 的前面
        pre.parentNode.insertBefore(parentDiv, pre);

        // 将 pre 移到新创建的 div 中
        parentDiv.appendChild(pre);

         // 将复制按钮添加到新创建的 div 中
         parentDiv.appendChild(copyCodeWrapper);
    });

    return doc.documentElement.innerHTML;
}


function formatDate(date, isSameDay) {
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const day = date.getDate();
    const month = date.getMonth() + 1;

    const hourFormat = hours < 10 ? '0' + hours : hours;
    const minuteFormat = minutes < 10 ? '0' + minutes : minutes;
    const time = `${hourFormat}:${minuteFormat}`;

    if (isSameDay) {
        return time;
    } else {
        return `${month}月${day}日 ${time}`;
    }
}

function timeDifference(date1, date2) {
    return Math.abs(date1 - date2) / 60000; // 返回分钟
}

function isSameDay(date1, date2) {
    if (!date1 || !date2) {
        return false;
    }
    return date1.getDate() === date2.getDate() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getFullYear() === date2.getFullYear();
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };

    return text.replace(/[&<>"']/g, function (m) {
        return map[m];
    });
}


function sendMessage() {
    const chatContent = document.getElementById('chat-content');
    const userInput = document.getElementById('messageInput');
    // const message = escapeHtml(userInput.value.trim());

    const message = userInput.value.trim();


    if (message.length > 0 && !isTyping) {
        isTyping = true;

        const userAvatar = '/static/img/girl.png';
        const replyAvatar = '/static/img/color.jpg';
        const userMessageId = `user-message-${Date.now()}`;
        const userMessage = `<div class="chat user" id="${userMessageId}"><span class="message">${escapeHtml(message)}</span><img src="${userAvatar}" alt="User"></div>`;
        const replyMessage = `<div class="chat reply" id="temporary-reply"><img src="${replyAvatar}" alt="Reply"><span class="message"><span class="placeholder-cursor"></span></span></div>`;

        // 移除上一个 temporary-reply 的 id
        if (document.getElementById('temporary-reply')) {
            document.getElementById('temporary-reply').removeAttribute('id');
        }

        // 获取当前时间和上一条用户消息的时间
        const now = new Date();
        let lastMessageTime = null;
        const lastMessageElements = document.querySelectorAll('.time[data-timestamp]');

        if (lastMessageElements.length > 0) {
            lastMessageTime = new Date(lastMessageElements[lastMessageElements.length - 1].getAttribute('data-timestamp'));
        }

        // 检查时间间隔是否超过10分钟
        const shouldShowTime = !lastMessageTime || (timeDifference(now, lastMessageTime) > 10);
        const formattedTime = formatDate(now, isSameDay(now, lastMessageTime));

        const timeElement = shouldShowTime ? `<div class="time" data-timestamp="${now}">${formattedTime}</div>` : '';


        // 添加新的聊天消息
        chatContent.insertAdjacentHTML('beforeend', timeElement + userMessage + replyMessage);


        chatContent.scrollTop = chatContent.scrollHeight;


        const selectedSite = localStorage.getItem('selectedSite');

        if (message && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                text: message,
                id: loadid(),
                miniid: loadminiid(),
                id360: loadid360(),
                site: selectedSite,
                lastmsg3list: loadmsg3(),
                lastmsg5list: loadmsg5(),
                lastmsg6list: loadmsg6(),
                lastmsg7list: loadmsg7(),
                lastmsg9list: loadmsg9(),
                lastmsg12list: loadmsg12(),
                lastmsg14list: loadmsg14(),
                lastmsg15list: loadmsg15(),

            }));
            userInput.value = '';
            resetAccumulatedText();
        }


        // 恢复输入框默认高度
        adjustTextareaHeight(userInput);
    }
}


function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey && !isMobileDevice()) {
        event.preventDefault(); // 阻止默认行为（换行）
        sendMessage();
        const messageInput = document.getElementById('messageInput');
        messageInput.value = '';
        setmessageInputsize();
    }
}

document.getElementById('messageInput').addEventListener('keydown', handleKeyDown); // 监听 keydown 事件


function deleteMessages() {
    const chatContent = document.getElementById('chat-content');
    const siteSelection = document.querySelector('.site-selection');

    // 删除chatContent的所有子元素，除了.site-selection
    let childNode = chatContent.firstChild;
    while (childNode) {
        if (childNode !== siteSelection) {
            const nextSibling = childNode.nextSibling;
            chatContent.removeChild(childNode);
            childNode = nextSibling;
        } else {
            childNode = childNode.nextSibling;
        }
    }

    localStorage.setItem('chatContent', 'DELETE'); // 将空字符串存储到localStorage中
    localStorage.setItem('lastmsg3list', '');
    localStorage.setItem('lastmsg5list', '');
    localStorage.setItem('lastmsg6list', '');
    localStorage.setItem('lastmsg7list', '');
    localStorage.setItem('lastmsg9list', '');
    localStorage.setItem('lastmsg12list', '');
    localStorage.setItem('lastmsg14list', '');
    localStorage.setItem('lastmsg15list', '');

    saveid('');
    saveminiid('');
    saveid360('');
}


function saveChatContent() {
    const chatContent = document.getElementById('chat-content');
    localStorage.setItem('chatContent', chatContent.innerHTML);
}

function loadnotice() {
    var lastPopupTime = localStorage.getItem('lastPopupTime');
    var currentTime = new Date().getTime();

    if (lastPopupTime && currentTime - lastPopupTime > 86400000) {
        showModal();
    }
    if (!lastPopupTime) {
        showModal();
    }
}


function loadChatContent() {
    const chatContent = document.getElementById('chat-content');
    const savedContent = localStorage.getItem('chatContent');

    if (savedContent && savedContent !== 'DELETE') {
        chatContent.innerHTML = savedContent;
        scrollToBottom();
    }

    const siteSelectDiv = document.getElementById('siteSelectDiv');

    //从localStorage中获取选项值，并设置为当前选项
    const savedValue = localStorage.getItem('selectedSite');

    if (savedValue) {
        for (const option of siteSelectDiv.children) {
            if (option.getAttribute('data-value') === savedValue) {
                //将匹配的选项设置为已选择,例如通过更改其样式
                setDropdownBtnText(option.textContent);
                break;
            }
        }
    }
}


function saveid(id) {
    if (!id) {
        localStorage.setItem('lastid', '');
    } else {
        localStorage.setItem('lastid', id);
    }
}

function saveminiid(id) {
    if (!id) {
        localStorage.setItem('miniid', '');
    } else {
        localStorage.setItem('miniid', id);
    }
}
function saveid360(id) {
    if (!id) {
        localStorage.setItem('id360', '');
    } else {
        localStorage.setItem('id360', id);
    }
}


function savelastmsg3list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg3list')) {
        list = JSON.parse(localStorage.getItem('lastmsg3list'));
    }

    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg3list', JSON.stringify(list));

}

function savelastmsg5list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg5list')) {
        list = JSON.parse(localStorage.getItem('lastmsg5list'));
    }
    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg5list', JSON.stringify(list));
}

function savelastmsg6list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg6list')) {
        list = JSON.parse(localStorage.getItem('lastmsg6list'));
    }
    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg6list', JSON.stringify(list));
}

function savelastmsg7list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg7list')) {
        list = JSON.parse(localStorage.getItem('lastmsg7list'));
    }
    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg7list', JSON.stringify(list));
}

function savelastmsg9list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg9list')) {
        list = JSON.parse(localStorage.getItem('lastmsg9list'));
    }
    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg9list', JSON.stringify(list));
}

function savelastmsg12list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg12list')) {
        list = JSON.parse(localStorage.getItem('lastmsg12list'));
    }

    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg12list', JSON.stringify(list));

}

function savelastmsg14list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg14list')) {
        list = JSON.parse(localStorage.getItem('lastmsg14list'));
    }

    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg14list', JSON.stringify(list));

}
function savelastmsg15list(msg) {
    let list = [];
    if (localStorage.getItem('lastmsg15list')) {
        list = JSON.parse(localStorage.getItem('lastmsg15list'));
    }

    if (list.length >= 10) {
        list.shift(); // 删除第一个元素
        list.shift(); // 再次删除第一个元素（原来的第二个元素）
    }

    list = list.concat(msg);

    localStorage.setItem('lastmsg15list', JSON.stringify(list));

}



function loadid() {
    const savedid = localStorage.getItem('lastid');
    if (savedid) {
        return savedid;
    }
    return "";
}

function loadminiid() {
    const savedid = localStorage.getItem('miniid');
    if (savedid) {
        return savedid;
    }
    return "";
}
function loadid360() {
    const savedid = localStorage.getItem('id360');
    if (savedid) {
        return savedid;
    }
    return "";
}

function loadmsg3() {
    const savedmsg = localStorage.getItem('lastmsg3list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}

function loadmsg5() {
    const savedmsg = localStorage.getItem('lastmsg5list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}

function loadmsg6() {
    const savedmsg = localStorage.getItem('lastmsg6list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}

function loadmsg7() {
    const savedmsg = localStorage.getItem('lastmsg7list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}

function loadmsg9() {
    const savedmsg = localStorage.getItem('lastmsg9list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}

function loadmsg12() {
    const savedmsg = localStorage.getItem('lastmsg12list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}

function loadmsg14() {
    const savedmsg = localStorage.getItem('lastmsg14list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}
function loadmsg15() {
    const savedmsg = localStorage.getItem('lastmsg15list');
    if (savedmsg) {
        return JSON.parse(savedmsg);
    }
    return "";
}




function linksblank() {
  var links = document.getElementsByTagName('a');
  for (var i = 0; i < links.length; i++) {
    links[i].setAttribute('target', '_blank');
  }
}




window.onload = function () {
    loadChatContent();
     linksblank();
     loadnotice();

}


function adjustTextareaHeight(textarea) {
// 记录当前滚动条位置
    const scrollTop = textarea.scrollTop;

// 重置输入框高度，以便正确计算新的滚动高度
    textarea.style.height = '100%';

// 计算新的输入框高度
    const maxHeight = textarea.parentElement.offsetHeight * 0.8;
    const newHeight = Math.min(textarea.scrollHeight, maxHeight);

// 更新输入框高度
    textarea.style.height = `${newHeight}px`;

// 还原滚动条位置
    textarea.scrollTop = scrollTop;
}

document.getElementById('messageInput').addEventListener('input', function () {
    adjustTextareaHeight(this);
});

const messageInput = document.getElementById('messageInput');
messageInput.addEventListener('focus', onFocus);
messageInput.addEventListener('blur', onBlur);

let resizeHandler;

function onFocus() {
    resizeHandler = () => {
        const chatContent = document.getElementById('chat-content');
        chatContent.scrollTop = chatContent.scrollHeight;
    };

    window.addEventListener('resize', resizeHandler);
}

function onBlur() {
    if (resizeHandler) {
        window.removeEventListener('resize', resizeHandler);
        resizeHandler = null;
    }
}


$(document).ready(function () {


    function setSelectedColorOption(option) {
        $(".color-option").removeClass("selected");
        $(option).addClass("selected");
    }

    $('.white').click(function () {
        $('body').removeClass('dark-theme').addClass('light-theme');
        localStorage.setItem('theme', 'light-theme');

        layer.config({
            extend: [],
        });

        setSelectedColorOption(this);
    });

    $('.black').click(function () {
        $('body').removeClass('light-theme').addClass('dark-theme');
        localStorage.setItem('theme', 'dark-theme');

        layer.config({
            extend: ['skin/layer-dark.css'],
        });

        setSelectedColorOption(this);
    });

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        $('body').removeClass('light-theme dark-theme').addClass(savedTheme);

        const selectedColorOption = savedTheme === "light-theme" ? ".white" : ".black";
        setSelectedColorOption($(selectedColorOption));
    }
});


function isMobileDevice() {
    return window.innerWidth <= 768;
}


function setmessageInputsize() {
    const messageInput = document.getElementById("messageInput");

    if (isMobileDevice()) {
        messageInput.style.height = '40px';
    } else {
        messageInput.style.height = '120px';
    }
}

function checkScreenWidth() {
    const parentElement = document.querySelector('.parent');

    if (isMobileDevice()) {
        parentElement.classList.add('collapsed');
        document.getElementById("messageInput").placeholder = "说点什么吧...  ";
    } else {
        parentElement.classList.remove('collapsed');
        document.getElementById("messageInput").placeholder = '说点什么吧...     Shift + Enter 换行    输入 "/" 弹出提问模板   输入 "/ + 关键词" 搜素模板';
    }


}

// 初始检查屏幕宽度
setmessageInputsize();
checkScreenWidth();

// 当窗口大小改变时，再次检查屏幕宽度
window.addEventListener('resize', () => {
    setmessageInputsize();
    checkScreenWidth();
    updateTemplatePopupPosition(); // 更新弹窗位置
    previousInnerHeight = window.innerHeight; // 更新 previousInnerHeight 值
});
document.getElementById("messageInput").addEventListener("input", function () {
    setmessageInputsize();
});

document.getElementById('toggleButton').addEventListener('click', function () {
    if (isMobileDevice()) {
        const parentElement = document.querySelector('.parent');
        parentElement.classList.toggle('collapsed');

    }
});


document.getElementById('shareButton').addEventListener('click', function () {
    showsModal();
});

document.getElementById('closeModal').addEventListener('click', function () {
    closesModal()
});

// 点击遮罩层时，关闭模态窗口
window.onclick = function (event) {
    if (event.target === document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
    }
};


const customContextMenu = document.getElementById("customContextMenu");
const copyOption = document.getElementById("copyOption");
const chatContent = document.getElementById("chat-content");

// 显示自定义右键菜单并选中消息文本
function showContextMenu(e) {
    let target = e.target.closest(".chat .message");

    // 如果没有点击 .chat .message 元素，返回并不显示上下文菜单
    if (!target) {
        customContextMenu.style.display = "none";
        return;
    }

    // 向上查找直到找到包含 'chat' 类的元素
    let chatElement = target;
    while (!chatElement.classList.contains('chat')) {
        chatElement = chatElement.parentElement;
    }

    // 如果 chatElement 没有 id，则为其生成一个唯一 id
    if (!chatElement.id) {
        chatElement.id = `chat-message-${Date.now()}`;
    }

    e.preventDefault();
    customContextMenu.style.display = "block";
    customContextMenu.style.left = `${e.clientX}px`;
    customContextMenu.style.top = `${e.clientY - customContextMenu.offsetHeight}px`;
    customContextMenu.dataset.target = chatElement.id;

    // 选中消息文本
    const range = document.createRange();
    range.selectNodeContents(target);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
}

function processNestedLists(item) {
    const parentList = item.parentElement;

    if (parentList.tagName === "OL") {
        const startIndex = parentList.hasAttribute("start")
            ? parseInt(parentList.getAttribute("start"))
            : 1;
        const index =
            Array.from(parentList.children).indexOf(item) + startIndex;
        item.innerHTML = `${index}.${item.innerHTML}`;
    } else if (parentList.tagName === "UL") {
        item.innerHTML = `· ${item.innerHTML}`;
    }

    // 处理嵌套列表
    const nestedItems = item.querySelectorAll("li");
    nestedItems.forEach((nestedItem) => processNestedLists(nestedItem));
}

// 复制消息文本并隐藏自定义右键菜单
function copyMessageText() {
    const targetId = customContextMenu.dataset.target;
    const targetElement = document.getElementById(targetId);
    const messageElement = targetElement.querySelector(".message");

    // 复制 messageElement
    const clonedMessageElement = messageElement.cloneNode(true);

    // 获取有序列表和无序列表的序号
    const listItems = clonedMessageElement.querySelectorAll("li");
    listItems.forEach((item) => processNestedLists(item));

    // 创建一个隐藏的可编辑元素，用于复制带格式的文本
    const hiddenEditableDiv = document.createElement("div");
    hiddenEditableDiv.contentEditable = "true";
    hiddenEditableDiv.style.position = "absolute";
    hiddenEditableDiv.style.left = "-9999px";
    hiddenEditableDiv.appendChild(clonedMessageElement);
    document.body.appendChild(hiddenEditableDiv);

    // 选中并复制带格式的文本
    const range = document.createRange();
    range.selectNodeContents(hiddenEditableDiv);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    document.execCommand("copy");

    layer.msg("复制成功!", {
        time: 500,
        offset: "100px",
        icon: 1,
    });

    // 移除隐藏的可编辑元素
    document.body.removeChild(hiddenEditableDiv);

    customContextMenu.style.display = "none";
}

function handleTouchStart(e) {
    const target = e.target.closest(".chat.user .message, .chat.reply .message");

    if (target) {
        e.preventDefault();
    }
}

function handleTouchEnd(e) {
    const touchEndTime = new Date().getTime();
    const longPressDuration = touchEndTime - touchStartTime;

    if (longPressDuration >= 500) {
        showContextMenu(e.changedTouches[0]);
    }
}

chatContent.addEventListener("contextmenu", showContextMenu);
document.body.addEventListener("click", () => customContextMenu.style.display = "none");
copyOption.addEventListener("click", copyMessageText);
document.addEventListener("touchstart", handleTouchStart, false);
document.addEventListener("touchend", handleTouchEnd, false);


const templatePopup = document.getElementById('templatePopup');

// 创建一个ul元素
const ul = document.createElement('ul');
templatePopup.appendChild(ul);

fetch('/static/templates.json').then((response) => response.json()).then((data) => {
    // 遍历JSON数据中的键值对并创建li元素
    for (const category in data) {
        if (data.hasOwnProperty(category)) {
            const sentences = data[category];
            sentences.forEach((templateSentence) => {
                const li = createLiElement(category, templateSentence);
                ul.appendChild(li);
            });
        }
    }
});

function createLiElement(category, templateSentence) {
    const categorySpan = document.createElement('span');
    categorySpan.textContent = `【${category}】`;
    categorySpan.style.color = '#5fcba8';

    const li = document.createElement('li');
    li.appendChild(categorySpan);
    li.append(templateSentence);

    // 添加点击事件监听器
    li.addEventListener('click', function () {
        messageInput.value = this.textContent.replace(`【${category}】`, '');
        templatePopup.style.display = 'none';
        messageInput.focus();
    });

    return li;
}

messageInput.addEventListener('input', function (event) {
    const firstCharIsSlash = messageInput.value.charAt(0) === '/';

    if (firstCharIsSlash && messageInput.value.length > 1) {
        // 提取关键词（去除"/"字符）
        const keyword = messageInput.value.slice(1).toLowerCase();

        // 遍历ul的所有子元素（li标签）
        for (const li of ul.children) {
            // 判断li标签中的文本是否包含关键词
            if (li.textContent.toLowerCase().includes(keyword)) {
                li.style.display = 'block';
            } else {
                li.style.display = 'none';
            }
        }
    } else if (firstCharIsSlash) {
        // 如果仅输入了"/"，则显示所有模板句子
        for (const li of ul.children) {
            li.style.display = 'block';
        }
    } else {
        templatePopup.style.display = 'none';
    }

    if (firstCharIsSlash) {
        // 显示弹窗并定位
        templatePopup.style.display = 'block';
        const inputRect = messageInput.getBoundingClientRect();
        templatePopup.style.left = inputRect.left + 'px';
        templatePopup.style.width = inputRect.width - 20 + 'px'; // 设置与输入框相同的宽度
        templatePopup.style.bottom = window.innerHeight - inputRect.top + 25 + 'px'; // 距离上方50px
    } else {
        templatePopup.style.display = 'none';
    }
});


// 添加一个点击事件监听器到文档对象
document.addEventListener('click', function (event) {
    var templatePopup = document.getElementById('templatePopup');
    var messageInput = document.getElementById('messageInput');

    // 检查事件目标是否在弹窗内部或为输入框
    if (!templatePopup.contains(event.target) && event.target !== messageInput) {
        // 隐藏弹窗
        templatePopup.style.display = 'none';
    }
});


// 添加一个点击事件监听器到输入框对象
messageInput.addEventListener('click', function (event) {
    const firstCharIsSlash = messageInput.value.charAt(0) === '/';

    if (firstCharIsSlash) {
        // 显示弹窗并定位
        templatePopup.style.display = 'block';
        const inputRect = messageInput.getBoundingClientRect();
        templatePopup.style.left = inputRect.left + 'px';
        templatePopup.style.width = inputRect.width - 20 + 'px'; // 设置与输入框相同的宽度
        templatePopup.style.bottom = window.innerHeight - inputRect.top + 25 + 'px'; // 距离上方50px
    } else {
        templatePopup.style.display = 'none';
    }
});


let previousInnerHeight = window.innerHeight;

function updateTemplatePopupPosition() {
    const firstCharIsSlash = messageInput.value.charAt(0) === '/';

    // 检查输入法是否收起
    if (window.innerHeight > previousInnerHeight) {
        templatePopup.style.display = 'none';
        return;
    }

    if (firstCharIsSlash) {
        // 显示弹窗并定位
        templatePopup.style.display = 'block';
        const inputRect = messageInput.getBoundingClientRect();
        templatePopup.style.left = inputRect.left + 'px';
        templatePopup.style.width = inputRect.width - 20 + 'px'; // 设置与输入框相同的宽度
        templatePopup.style.bottom = window.innerHeight - inputRect.top + 25 + 'px'; // 距离上方50px
    } else {
        templatePopup.style.display = 'none';
    }
}


const noticeButton = document.getElementById("noticeButton");
const acknowledged = document.getElementById("acknowledged");
const colorPickerModal = document.getElementById("colorPickerModal");
const myModal = document.getElementById("myModal");
const closeColorPickerModal = document.getElementById("closeColorPickerModal");


// 当点击齿轮图标时，显示颜色选择器弹窗


noticeButton.addEventListener("click", () => {
    myModal.style.display = "block";
});

acknowledged.addEventListener("click", () => {
     closeModal();
     localStorage.setItem('lastPopupTime', new Date().getTime());
});

// 当点击关闭按钮时，隐藏颜色选择器弹窗
closeColorPickerModal.addEventListener("click", () => {
    closeModalsetting();
});


document.querySelector('.dropdown-btn').addEventListener('click', function () {
    var dropdownContent = document.querySelector('.dropdown-content');
    if (dropdownContent.style.display === 'block') {
        dropdownContent.style.display = 'none';
    } else {
        dropdownContent.style.display = 'block';
    }
});

// 获取所有的<div>选项元素
var divItems = document.querySelectorAll('.dropdown-content > div');

// 为每个<div>选项元素添加点击事件监听器，更新原始<select>元素的值
divItems.forEach(function (divItem) {
    divItem.addEventListener('click', function () {

        setDropdownBtnText(this.innerText);
        layer.msg('模型切换成功!', {
            time: 500, // 设置显示时间，单位为毫秒
            offset: '100px', // 设置距离顶部的距离
            icon: 1,
        });
        // 隐藏下拉菜单内容
        document.querySelector('.dropdown-content').style.display = 'none';
    });
});

//当用户点击选项时,将其值存储到localStorage中并更新样式
function getOptionValue(element) {
    var dataValue = element.getAttribute('data-value');
    localStorage.setItem('selectedSite', dataValue);

    // 更新 "请选择" 文字
    setDropdownBtnText(element.textContent);
}

// 设置 "请选择" 文字的函数
function setDropdownBtnText(text) {
    const dropdownBtn = document.getElementById('dropdownBtn');

    // 更新 "请选择" 文字
    dropdownBtn.childNodes[0].textContent = text;

}

function setDefaultOption() {
    var defaultOption = document.querySelector('.default-option');
    var dropdownBtn = document.getElementById('dropdownBtn');
    dropdownBtn.innerHTML = defaultOption.innerHTML + '<span id="arrowIcon">' + arrowIcon.innerHTML + '</span>';
    var dataValue = defaultOption.getAttribute('data-value');
    localStorage.setItem('selectedSite', dataValue);
}
document.addEventListener('DOMContentLoaded', function () {
    var savedOption = localStorage.getItem('selectedSite');
    if (!savedOption) {
    setDefaultOption();}
});



function showModal() {
    const myModal = document.getElementById('myModal');
    myModal.style.display = "block";
    // 在显示弹窗前添加modal-show类
    setTimeout(() => {
        myModal.classList.add('modal-show');
    }, 0);
}

function closeModal() {
    const myModal = document.getElementById('myModal');
    // 在隐藏弹窗前移除modal-show类
    myModal.classList.remove('modal-show');
    // 因为过渡效果需要时间，所以我们在过渡结束后再隐藏弹窗
    setTimeout(() => {
        myModal.style.display = "none";
    }, 300);  // 这个300毫秒应该与你在CSS中设置的过渡时间相同
}
function closeModalsetting() {
    const colorPickerModal = document.getElementById('colorPickerModal');
    // 在隐藏弹窗前移除modal-show类
    colorPickerModal.classList.remove('custom-modal-show');
    // 因为过渡效果需要时间，所以我们在过渡结束后再隐藏弹窗
    setTimeout(() => {
        colorPickerModal.style.display = "none";
    }, 300);  // 这个300毫秒应该与你在CSS中设置的过渡时间相同
}

function showModalsetting() {
    const colorPickerModal = document.getElementById('colorPickerModal');
    colorPickerModal.style.display = "block";
    // 在显示弹窗前添加modal-show类
    setTimeout(() => {
        colorPickerModal.classList.add('custom-modal-show');
    }, 0);
    var dropdownContent = document.getElementById("siteSelectDiv");
        dropdownContent.style.display = "none";
}

function showsModal() {
    const myModal = document.getElementById('modal');
    myModal.style.display = "block";
    // 在显示弹窗前添加modal-show类
    setTimeout(() => {
        myModal.classList.add('modal-show');
    }, 0);
}

function closesModal() {
    const myModal = document.getElementById('modal');
    // 在隐藏弹窗前移除modal-show类
    myModal.classList.remove('modal-show');
    // 因为过渡效果需要时间，所以我们在过渡结束后再隐藏弹窗
    setTimeout(() => {
        myModal.style.display = "none";
    }, 300);  // 这个300毫秒应该与你在CSS中设置的过渡时间相同
}

document.getElementById('settingsButton').addEventListener('click', showModalsetting);
document.getElementById('noticeButton').addEventListener('click', showModal);
document.getElementById('closeModal1').addEventListener('click', closeModal);


function handleClickOutside(event) {
  var modal1 = document.getElementById('colorPickerModal');
  var modal2 = document.getElementById('myModal');
  if (event.target == modal1) {
    closeModalsetting();
  }
  if (event.target == modal2) {
    closeModal();
  }
}


function resetStyles() {
  messageInput.style.position = '';
  messageInput.style.bottom = '';
  messageInput.style.marginBottom = '';
  messageInput.style.width = '';
  messageInputWrapper.style.height = '';
  messageInputWrapper.style.bottom = '';
}


const messageInputWrapper = document.getElementById('messageInputWrapper');
const sendButton = document.getElementById('sendButton');

function updateMessageInputPosition() {
const windowHeight = window.innerHeight;
const wrapperRect = messageInputWrapper.getBoundingClientRect();

 resetStyles();

if (wrapperRect.bottom > windowHeight) {
  messageInput.style.position = 'fixed';
  if (isMobileDevice()) {
      messageInput.style.bottom = '10px';
      messageInput.style.marginBottom = "30px"
      messageInput.style.width = "calc(100% - 85px)"
      messageInput.style.paddingRight = "60px"
      messageInputWrapper.style.height = "0"
      messageInputWrapper.style.bottom = '10px';
       sendButton.style.marginTop = "-60px"
      sendButton.style.marginRight = "calc(-100% + 60px)"


  } else {
        messageInput.style.bottom = '20px';
        messageInput.style.marginBottom = "0"
       messageInput.style.paddingRight = "80px"
      sendButton.style.marginTop = "100px"
      sendButton.style.marginRight = "calc(-100% + 80px)"

  }
} else {
  messageInput.style.position = 'absolute';
  if (isMobileDevice()) {
      messageInput.style.bottom = '10px';
      messageInput.style.marginBottom = "30px"
      messageInput.style.width = "calc(100% - 85px)"
      messageInput.style.paddingRight = "60px"
      messageInputWrapper.style.height = "0"
      messageInputWrapper.style.bottom = '10px';
        sendButton.style.marginTop = "-60px"
      sendButton.style.marginRight = "calc(-100% + 60px)"
  } else {
  messageInput.style.bottom = '20px';
  messageInput.style.paddingRight = "80px"
  messageInput.style.marginBottom = "0";
  sendButton.style.marginTop = "100px"
  sendButton.style.marginRight = "calc(-100% + 80px)"
  }
}
}

window.addEventListener('resize', updateMessageInputPosition);
updateMessageInputPosition();



function checkInput() {
  if (messageInput.value.length > 0) {
    sendButton.style.background = "linear-gradient(to right, #77a7e7, #ea607b)";
  } else {
    sendButton.style.background  = "#8bcfab";
  }
}

sendButton.addEventListener('click', function() {
    sendMessage();
    const messageInput = document.getElementById('messageInput');
    messageInput.value = '';
    sendButton.style.background  = "#8bcfab";
    setmessageInputsize();
});
