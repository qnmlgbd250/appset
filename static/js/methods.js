function headersTransform(inputText) {
    if (!inputText.trim()) {
        return '';
    }
    let headerDict = {};
    let lastKey = null;
    let splitStrList = inputText.split("\n");
    for (let index = 0; index < splitStrList.length; index++) {
        if (splitStrList[index].endsWith(":")) {
            splitStrList[index] = splitStrList[index] + splitStrList[index + 1];
            splitStrList[index + 1] = "";
        }
    }
    let formatList = splitStrList.filter(x => x);
    for (let line of formatList) {
        if (line.trim() === "") {
            continue;
        }
        if (/[A-Za-z0-9\-]+:/.test(line)) {
            let colonIndex = line.indexOf(':')
            lastKey = line.substring(0, colonIndex).trim();
            headerDict[lastKey] = line.substring(colonIndex + 1).trim();
        } else if (lastKey != null) {
            headerDict[lastKey] += line.trim();
        }
    }
    return JSON.stringify(headerDict, null, 4);
}

function cookieTransform(inputText) {

// 如果输入为空，将输出清空并返回
    if (!inputText.trim()) {
        return '';
    }

    const cookies = inputText.split(';').reduce((acc, line) => {
        const [key, value] = line.split('=');
        if (key && value) {
            acc[key.trim()] = value.trim();
        }
        return acc;
    }, {});

    return JSON.stringify(cookies, null, 2);
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
    return rsa.decrypt(inputText);
}

//curl转换主函数
function curlTransform(inputText) {
    return new Promise((resolve, reject) => {
        const url = '/tool/c';
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
                resolve(data.output.replace(/\\n/g, "\n")); // 将返回的数据作为Promise的解析值
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                reject(error); // 如果发生错误，则将Promise标记为拒绝状态，并传递错误信息
            });
    });
}


//Data转换主函数
function dataTransform(inputText) {
    return new Promise((resolve, reject) => {
        inputText = inputText.trim();
        if (!inputText) {
            return;
        }
        const url = '/tool/d/';
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
                resolve(JSON.stringify(JSON.parse(data.output), null, 2)); // 将返回的数据放入output元素中
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                reject(error);
            });

        localStorage.setItem('taskid', inputText);
    });
}

function smsTransform(inputText) {
    return new Promise((resolve, reject) => {
        inputText = inputText.trim();
        if (!inputText) {
            return;
        }
        const url = '/tool/s/';
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
                resolve(JSON.stringify(data.output, null, 2)); // 将返回的数据放入output元素中
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                reject(error);
            });
    });
}


//翻译主函数
function transTransform(inputText) {
    return new Promise((resolve, reject) => {
        inputText = inputText.trim();
        if (!inputText) {
            return;
        }
        const url = '/tool/t';
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
                if (data.output && typeof data.output === 'object' && Object.keys(data.output).length === 0) {
                    resolve(''); // 如果data.output是空对象，则返回空字符串
                } else {
                    resolve(data.output); // 否则返回data.output

                }// 将返回的数据放入output元素中
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    });
}


//签到计算主函数
function signTransform(inputText) {
    inputText = inputText.replace(/\s/g, '');

    // 如果输入为空，将输出清空并返回
    if (!inputText.trim()) {
        return '';
    }

    const regex = /^(\d{1,2})[:：](\d{1,2})$/;
    const match = inputText.match(regex);

    if (!match) {
        return '输入格式有误，请输入正确的时间格式（HH:MM）';
    }

    const input_time = inputText.replace(/[：:]/g, ':');
    const [HH, MM] = input_time.split(':').map(Number);

    if (HH < 0 || HH > 24 || MM >= 60) {
        layer.msg('非预期的时间(你这输入的是三体时间吗？)', {
            time: 3000, // 设置显示时间，单位为毫秒
            // skin: getLayerSkin(), // 设置样式
            offset: '100px', // 设置距离顶部的距离
            icon: 2,
        });
        return '';

    }

    if (HH < 8 || (HH === 8 && MM < 30)) {
        return '正常打卡时间在 8:30 之后';
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
        return '输入时间范围有误，请输入正确的时间格式（HH:MM）';
    }

    let total_minutes = HH * 60 + MM;

    let new_total_minutes = (total_minutes + four_offset_minutes) % (24 * 60);
    let new_HH = Math.floor(new_total_minutes / 60);
    let new_MM = new_total_minutes % 60;
    let four_s = `4工时打卡时间为：${new_HH.toString().padStart(2, '0')}:${new_MM.toString().padStart(2, '0')}`;

    new_total_minutes = (total_minutes + eight_offset_minutes) % (24 * 60);
    new_HH = Math.floor(new_total_minutes / 60);
    new_MM = new_total_minutes % 60;
    return four_s + `\n8工时打卡时间为：${new_HH.toString().padStart(2, '0')}:${new_MM.toString().padStart(2, '0')}`;

}


//OCR主函数
function ocrTransform(input) {
    return new Promise((resolve, reject) => {
        const imgRegex = /<img.*?src=["'](.*?)["'].*?>/i;
        const match = imgRegex.exec(input);
        if (match && match[1]) {
            inputText = match[1];
        }
        if (!inputText) {
            return
        }
        const url = '/tool/o';
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
                resolve(data.output) // 将返回的数据放入output元素中
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    });
}

