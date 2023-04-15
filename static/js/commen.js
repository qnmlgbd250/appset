//定义全局变量
const input = document.getElementById('input');
const output = document.getElementById('output');
const ocrBtn = document.getElementById('ocrBtn');
const chatBtn = document.getElementById('chatBtn');
const clearBtn = document.getElementById('clearBtn');
const copyBtn = document.getElementById('copyBtn');
const menuFunctions = {
    'headerBtn': headersTransform,
    'cookieBtn': cookieTransform,
    'curlBtn': curlTransform,
    'rsaBtn': rsaTransform,
    'dataBtn': dataTransform,
    'transBtn': transTransform,
    'signBtn': signTransform,
    'ocrBtn': ocrTransform,

    // 添加更多功能函数...
};


//菜单方法-选中突出显示
var divs = document.querySelectorAll(".menu-div");

for (var i = 0; i < divs.length; i++) {
    divs[i].onclick = function () {
        var allDivs = document.querySelectorAll(".menu-div");
        for (var j = 0; j < allDivs.length; j++) {
            allDivs[j].classList.remove("selected");
        }
        this.classList.add("selected");
        input.value = "";
        output.value = "";
        imageContainer.innerHTML = '';
        showChatBox(false);
        if (this.id !== 'ocrBtn') {
            input.style.display = 'block';
            imageContainer.style.display = 'none';
            imageContainer.removeEventListener('paste', handlePaste);
        }
    };
}


//主题颜色方法-点击按钮改变输入输出的边框颜色
const inputBox = document.getElementById("input");
const imgBox = document.getElementById("image-container");
const outputBox = document.getElementById("output");
const buttons = document.querySelectorAll("button");

buttons.forEach(button => {
    button.addEventListener("click", () => {
        inputBox.style.borderColor = button.className;
        outputBox.style.borderColor = button.className;
        imgBox.style.borderColor = button.className;

    });
});


//
document.addEventListener('DOMContentLoaded', () => {

    const menuDivs = document.querySelectorAll('.menu-div');


    menuDivs.forEach(menuDiv => {
        menuDiv.addEventListener('click', () => {
            // 移除所有菜单项的选中状态
            menuDivs.forEach(m => m.classList.remove('selected'));

            // 为当前点击的菜单项添加选中状态
            menuDiv.classList.add('selected');


        });
    });

    // 为输入框添加输入事件监听器
    input.addEventListener('input', () => {
        tryExecuteMenuFunction();
    });

    function tryExecuteMenuFunction() {
        // 检查选中的菜单项是否有对应的功能函数
        const selectedMenu = document.querySelector('.menu-div.selected');
        if (selectedMenu && input.value.trim() !== '') {
            const menuFunction = menuFunctions[selectedMenu.id];
            if (menuFunction) {
                menuFunction(input.value);
            }
        }
    }
});

//headers转换主函数
function headersTransform(inputText) {
    // 如果输入为空，将输出清空并返回
    if (!inputText.trim()) {
        output.value = '';
        return;
    }
    const headers = parseHeaders(inputText);
    output.value = JSON.stringify(headers, null, 2);
}

// 解析 HTTP 请求头字符串
function parseHeaders(headerStr) {
    const lines = headerStr.split(/\r?\n/);
    const headers = {};

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const index = line.indexOf(':');
        if (index !== -1) {
            const key = line.slice(0, index).trim();
            const value = line.slice(index + 1).trim();
            if (headers[key]) {
                headers[key] += ', ' + value;
            } else {
                headers[key] = value;
            }
        }
    }

    return headers;
}

//Cookie转换主函数
function cookieTransform(inputText) {

// 如果输入为空，将输出清空并返回
    if (!inputText.trim()) {
        output.value = '';
        return;
    }

    const cookies = inputText.split(';').reduce((acc, line) => {
        const [key, value] = line.split('=');
        if (key && value) {
            acc[key.trim()] = value.trim();
        }
        return acc;
    }, {});

    output.value = JSON.stringify(cookies, null, 2);
}

//RSA转换主函数
function rsaTransform(inputText) {
    const privateKey = '-----BEGIN RSA PRIVATE KEY-----\n' +
        'MIICXQIBAAKBgQCnUM8ytq3umKWdiUYRNzo+e3HhfPbFkJ60twdvTudHxBLkssF0\n' +
        'TWfUpzlGTT/yCEwvnF9jdjq568dYWO4+1Sdk5bom4Mm0Q+xsv4vLL7Vby7DkipL0\n' +
        'cRAT9sJv9n5cuFVgCvkiqWHzDX7SK1n2CVEMybhlBNOfVptTYISCSN5udwIDAQAB\n' +
        'AoGAFGQJzGFtEx3xWSCotGJpq8G5oERtgqhcXyPLOSqBj0J7FvoeD4F7fPQgS8wQ\n' +
        'Vfvi5Q6GpYV8JLpyYfb8mhW6JiQvj4mUZQNLvPm54AgRG6+ZzlTquawdJc9io9OK\n' +
        '6B4TU7JEXn0vGKVz6ZqH4SYLUKHHSKSTaQRX1tM8zOBm5uECQQDe5vmd5urdpb5B\n' +
        'BHE1iiWzeHxTWebE7LLlnnN2k0uC6WjGnbAXFn2L7tP51/LMRbyKhBwOrVZJu20/\n' +
        'eUSvTr7nAkEAwCjcY61mqC7j6QKyFxt7TeyCihNfkhXrc2XYuUSZfqWBtoZPGqhZ\n' +
        '9Kz3WiJpW90KZwQARZrfMK5v6yTxV2mx8QJBAJB9BL24W/KFZ8hZitD71eh6Z4zY\n' +
        'L+Di1ixGA+6PGFmp14M34Fd2+rbkf3/q3bZQViEr9cwFzHNLDUwh3cYNs20CQBXJ\n' +
        'zEuFEtnJD1CRXK4gEJgiVB7h2XlQAPWBu9QuAhWJIK8YhYmpQyHqJtXShw3Cf3Z0\n' +
        'zq8Vw27aqJgKBU97DZECQQDedmYTpRp0SXb3oUlMXuLhypDNXOG6Sb1kROVCQzAu\n' +
        'lkT3KLOjoCv4zVvQJkRg1X8FgzP/qRESc797fQfRmYmI\n' +
        '-----END RSA PRIVATE KEY-----';
    const rsa = new JSEncrypt();
    rsa.setPrivateKey(privateKey);
    output.value = rsa.decrypt(inputText);
}

//curl转换主函数
function curlTransform(inputText) {

    const url = '/c';
    fetch(url, {
        method: 'POST',
        body: JSON.stringify({input_str: inputText})
    })
        .then(response => {
            if (response.ok) {
                return response.json(); // 将response对象转换为JSON格式
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            console.log(data); // 输出JSON格式的数据
            output.value = data.output.replace(/\\n/g, "\n") // 将返回的数据放入output元素中
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

//Data转换主函数
function dataTransform(inputText) {
    inputText = inputText.trim();
    const url = '/d/';
    fetch(url + inputText)
        .then(response => {
            if (response.ok) {
                return response.json(); // 将response对象转换为JSON格式
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            console.log(data); // 输出JSON格式的数据
            output.value = JSON.stringify(JSON.parse(data.output), null, 2); // 将返回的数据放入output元素中
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });

}

let timeoutId;

function transTransform(input) {
    // 取消前一个setTimeout
    clearTimeout(timeoutId);

    // 1秒后触发翻译请求
    timeoutId = setTimeout(function () {
        // 调用翻译API
        translate(input);
    }, 500);
}

//翻译主函数
function translate(inputText) {
    inputText = inputText.trim();
    const url = '/t/';
    fetch(url + inputText)
        .then(response => {
            if (response.ok) {
                return response.json(); // 将response对象转换为JSON格式
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            console.log(data); // 输出JSON格式的数据
            output.value = data.output // 将返回的数据放入output元素中
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });

}

//签到计算主函数
function signTransform(inputText) {
    inputText = inputText.replace(/\s/g, '');

    // 如果输入为空，将输出清空并返回
    if (!inputText.trim()) {
        output.value = '';
        return;
    }

    const regex = /^(\d{1,2})[:：](\d{1,2})$/;
    const match = inputText.match(regex);

    if (!match) {
        output.value = '输入格式有误，请输入正确的时间格式（HH:MM）';
        return;
    }

    const input_time = inputText.replace(/[：:]/g, ':');
    const [HH, MM] = input_time.split(':').map(Number);

    if (HH < 0 || HH > 24 || MM >= 60) {
        layer.msg('非预期的时间(你这输入的是三体时间吗？)', {
            time: 3000, // 设置显示时间，单位为毫秒
            skin: 'layui-layer-lan', // 设置样式
            offset: '100px', // 设置距离顶部的距离
            icon: 2,
        });
        output.value = '';
        return;

    }

    if (HH < 8 || (HH === 8 && MM < 30)) {
        output.value = '正常打卡时间在 8:30 之后';
        return;
    }

    let four_offset_minutes = 0;
    let eight_offset_minutes = 0;

    if ((HH === 8 && MM >= 30) || (HH > 8 && HH < 12) || (HH === 12 && MM < 15)) {
        four_offset_minutes = 5 * 60 + 15;
        eight_offset_minutes = 9 * 60 + 15;
    } else if ((HH === 12 && MM >= 15) || (HH > 12 && HH < 13) || (HH === 13 && MM < 30)) {
        four_offset_minutes = (13 * 60 + 30 - HH * 60 - MM + 4 * 60) % (24 * 60);
        eight_offset_minutes = (13 * 60 + 30 - HH * 60 - MM + 8 * 60) % (24 * 60);
    } else if ((HH === 13 && MM >= 30) || (HH > 13)) {
        four_offset_minutes = 4 * 60;
        eight_offset_minutes = 8 * 60;
    } else {
        output.value = '输入时间范围有误，请输入正确的时间格式（HH:MM）';
        return;
    }

    let total_minutes = HH * 60 + MM;

    let new_total_minutes = (total_minutes + four_offset_minutes) % (24 * 60);
    let new_HH = Math.floor(new_total_minutes / 60);
    let new_MM = new_total_minutes % 60;
    let four_s = `4工时打卡时间为：${new_HH.toString().padStart(2, '0')}:${new_MM.toString().padStart(2, '0')}`;

    new_total_minutes = (total_minutes + eight_offset_minutes) % (24 * 60);
    new_HH = Math.floor(new_total_minutes / 60);
    new_MM = new_total_minutes % 60;
    output.value = four_s + `\n8工时打卡时间为：${new_HH.toString().padStart(2, '0')}:${new_MM.toString().padStart(2, '0')}`;
}


//OCR主函数
function ocrTransform(input) {
    inputText = input.querySelector('img').getAttribute('src').trim();
    const url = '/o';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        },
        body: JSON.stringify({image: inputText})
    })
        .then(response => {
            if (response.ok) {
                return response.json(); // 将response对象转换为JSON格式
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            console.log(data); // 输出JSON格式的数据
            output.value = data.output // 将返回的数据放入output元素中
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}


function handlePaste(e) {
    const items = e.clipboardData.items;
    let isImagePasted = false;

    for (const item of items) {
        if (item.type.indexOf('image') !== -1) {
            e.preventDefault(); // 阻止默认的粘贴行为
            isImagePasted = true;

            const img = new Image();
            const reader = new FileReader();

            reader.onload = (event) => {
                img.src = event.target.result;
                img.onload = () => {
                    imageContainer.innerHTML = ''; // 清空已有图片
                    imageContainer.appendChild(img); // 添加新图片
                    ocrTransform(imageContainer); // 调用OCR转换函数

                    // 创建一个空的文本节点并将其添加到 image-container 的末尾
                    const textNode = document.createTextNode('');
                    imageContainer.appendChild(textNode);

                    // 将光标设置到空的文本节点
                    const range = document.createRange();
                    range.selectNodeContents(textNode);
                    range.collapse(false);

                    const selection = window.getSelection();
                    selection.removeAllRanges();
                    selection.addRange(range);
                };
            };
            reader.readAsDataURL(item.getAsFile());
            break;
        }
    }

    if (!isImagePasted) {
        e.preventDefault(); // 在此处添加阻止默认粘贴行为，以禁止粘贴文本
        layer.msg('请粘贴图片，文字输入已被禁止', {
            time: 2000, // 设置显示时间，单位为毫秒
            skin: 'layui-layer-lan', // 设置样式
            offset: '100px', // 设置距离顶部的距离
            icon: 2,
        });
    }
}


const imageContainer = document.getElementById('image-container');
ocrBtn.addEventListener('click', () => {
    ocrshow(true);
});

function ocrshow(show) {
    if (show) {
        input.style.display = 'none';
        imageContainer.style.display = 'block';
        imageContainer.addEventListener('paste', handlePaste);
    } else {
        input.style.display = 'block';
        imageContainer.style.display = 'none';
        imageContainer.removeEventListener('paste', handlePaste);
    }
}


function showChatBox(show) {
    const chatContent = document.getElementById('chat-content');
    const div3 = document.getElementById('div3');
    const div4 = document.getElementById('div4');
    const div6 = document.getElementById('div6');
    const output = document.getElementById('output');
    if (show) {
        div3.style.display = 'none';
        div3.style.border = 'none';
        div4.style.border = 'none';
        div4.style.display = 'block';
        div6.style.display = 'block';
        output.style.display = 'none';
        chatContent.style.display = 'block';
    } else {
        div3.style.display = 'block';
        div3.style.borderRight = '1px solid #ccc';
        div4.style.borderLeft = '1px solid #ccc';
        div4.style.display = 'block';
        div6.style.display = 'none';
        output.style.display = 'block';
        chatContent.style.display = 'none';
    }
}

chatBtn.addEventListener('click', () => {
    showChatBox(true);
    const chatBox = document.getElementById("chat-content");
    chatBox.scrollTop = chatBox.scrollHeight - chatBox.clientHeight;
});

// 恢复样式


clearBtn.addEventListener('click', () => {
    input.value = '';
    output.value = '';
    const selectedid = document.querySelector('.menu-div.selected').id
    if (selectedid === 'chatBtn') {
        deleteMessages();
    }
    if (selectedid === 'ocrBtn') {
        imageContainer.innerHTML = '';
    }

});
copyBtn.addEventListener('click', () => {
    // 如果输出框没有文本内容，弹出提示
    if (!output.value) {
        layer.msg('输出框为空，无法复制', {offset: [$(window).height() - 450], icon: 2, time: 1000});
        return;
    }
    // 选中输出框的文本内容
    output.select();
    // 执行复制命令
    document.execCommand('copy');
    // 弹出成功提示
    layer.msg('复制成功!', {
        time: 2000, // 设置显示时间，单位为毫秒
        skin: 'layui-layer-lan', // 设置样式
        offset: '100px', // 设置距离顶部的距离
        icon: 1,
    });
});


let isTyping = false;
const host = window.location.hostname;
const port = window.location.port;
const url = `ws://${host}:${port}/chat`;

let socket = null;
let retryCount = 0; // 记录重连次数
let isReconnecting = false; // 标记是否正在重连

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
        const replyElement = document.getElementById('temporary-reply').querySelector('.message');
        const blinkElement = replyElement.querySelector('.placeholder-cursor');
        const chatContent = document.getElementById('chat-content');
        const userInput = document.getElementById('messageInput');

        // 创建一个监听 element 内容更改的 MutationObserver
        const observer = new MutationObserver(() => {
            chatContent.scrollTop = chatContent.scrollHeight;
        });

        // 开始监听 element 的子节点变化
        observer.observe(replyElement, {childList: true});
        if (receivedData) {
            isTyping = false;
            replyElement.style.whiteSpace = 'pre-line';
            // 添加接收到的文本
            const textNode = document.createElement('span');
            textNode.textContent = receivedData.text;
            replyElement.insertBefore(textNode, blinkElement);

            // 移除光标
            blinkElement.remove();

            chatContent.scrollTop = chatContent.scrollHeight;
            blinkElement.classList.remove('blink'); // 去除闪烁光标
            userInput.focus();

            if (receivedData.id) {
                saveid(receivedData.id)
            }
            // 停止监听 element 的子节点变化
            observer.disconnect();

        }
        saveChatContent(); //
        // typeReply(replyElement, receivedData.text, chatContent, blinkElement);
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
            // 添加接收到的文本
            const textNode = document.createElement('span');
            textNode.textContent = '异常断开，请重新键入';
            replyElement.insertBefore(textNode, blinkElement);

            // 移除光标
            blinkElement.remove();

            chatContent.scrollTop = chatContent.scrollHeight;
            blinkElement.classList.remove('blink'); // 去除闪烁光标
            userInput.focus();


            setTimeout(connect, retryInterval); // 定时器中执行重连
            retryCount++; // 增加重连次数
        }
    });


    socket.addEventListener('error', (event) => {
        console.error('WebSocket error:', event);
    });
}

// 初始化连接
connect();


function sendMessage() {
    const chatContent = document.getElementById('chat-content');
    const userInput = document.getElementById('messageInput');
    const message = escapeHtml(userInput.value.trim());

    if (message.length > 0 && !isTyping) {
        isTyping = true;

        const userAvatar = '/static/img/user.png';
        const replyAvatar = '/static/img/chat.png';
        const userMessage = `<div class="chat user"><span class="message">${message}</span><img src="${userAvatar}" alt="User"></div>`;
        const replyMessage = `<div class="chat reply" id="temporary-reply"><img src="${replyAvatar}" alt="Reply"><span class="message"><span class="placeholder-cursor"></span></span></div>`;

        // 移除上一个 temporary-reply 的 id
        if (document.getElementById('temporary-reply')) {
            document.getElementById('temporary-reply').removeAttribute('id');
        }

// 添加新的聊天消息
        chatContent.insertAdjacentHTML('beforeend', userMessage + replyMessage);

        chatContent.scrollTop = chatContent.scrollHeight;

        if (message && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({text: message, id: loadid()}));
            userInput.value = '';
        }


        // 恢复输入框默认高度
        adjustTextareaHeight(userInput);
    }
}


function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // 阻止默认行为（换行）
        sendMessage();
        const messageInput = document.getElementById('messageInput');
        messageInput.value = '';
    }
}

document.getElementById('messageInput').addEventListener('keydown', handleKeyDown); // 监听 keydown 事件


function deleteMessages() {
    const chatContent = document.getElementById('chat-content');
    chatContent.innerHTML = '';
    saveChatContent();
    saveid('')// 保存空的聊天记录以覆盖之前的记录
}


function saveChatContent() {
    const chatContent = document.getElementById('chat-content');
    localStorage.setItem('chatContent', chatContent.innerHTML);
}

function loadChatContent() {
    const chatContent = document.getElementById('chat-content');
    const savedContent = localStorage.getItem('chatContent');
    if (savedContent) {
        chatContent.innerHTML = savedContent;
    }
}

function saveid(id) {
    localStorage.setItem('lastid', id);
}

function loadid() {
    const savedid = localStorage.getItem('lastid');
    if (savedid) {
        return savedid;
    }
    return "";
}

window.onload = function () {
    loadChatContent(); // 加载聊天记录
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











