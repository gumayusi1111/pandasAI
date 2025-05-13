document.addEventListener('DOMContentLoaded', function() {
    // 在页面加载完成后将右侧内容区域向下滚动200px
    setTimeout(() => {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.scrollTop = 200;
        }
        
        // 如果主内容区域不滚动，尝试使用window滚动
        if (mainContent && mainContent.scrollTop === 0) {
            window.scrollTo(0, 200);
        }
    }, 100); // 短暂延迟确保DOM完全加载
    
    // Elements
    const generateForm = document.getElementById('generate-form');
    const modelSelect = document.getElementById('model');
    const csvFileInput = document.getElementById('csv-file');
    const fileNameDisplay = document.getElementById('file-name');
    const queryInput = document.getElementById('query');
    const generateBtn = document.getElementById('generate-btn');
    const clearBtn = document.getElementById('clear-btn');
    const copyBtn = document.getElementById('copy-btn');
    const codeOutput = document.getElementById('code-output');
    const errorMessage = document.getElementById('error-message');
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    const historyList = document.getElementById('history-list');
    const copyNotification = document.getElementById('copy-notification');
    
    // 进度条元素
    const progressContainer = document.getElementById('progress-container');
    const progressBarFill = document.getElementById('progress-bar-fill');
    const progressPercentage = document.getElementById('progress-percentage');
    const progressTokens = document.getElementById('progress-tokens');
    
    // 模拟进度状态
    let progressInterval;
    let currentProgress = 0;
    let estimatedTokens = 0;
    const totalTokensEstimate = 1000; // 预估的最大token数量
    
    // Initialize highlight.js
    hljs.highlightAll();
    
    // Load history when the page loads
    loadHistory();
    
    // 开始进度条动画
    function startProgressAnimation() {
        // 显示进度条
        progressContainer.classList.add('active');
        progressBarFill.style.width = '0%';
        progressPercentage.textContent = '0%';
        progressTokens.textContent = '0 tokens';
        
        currentProgress = 0;
        estimatedTokens = 0;
        
        // 清除之前的计时器（如果有）
        if (progressInterval) {
            clearInterval(progressInterval);
        }
        
        // 设置计时器以更新进度
        progressInterval = setInterval(() => {
            // 模拟渐进式进度增长，速度随着进度的增加而变慢
            if (currentProgress < 30) {
                currentProgress += 1.5;
            } else if (currentProgress < 60) {
                currentProgress += 0.8;
            } else if (currentProgress < 85) {
                currentProgress += 0.3;
            } else if (currentProgress < 95) {
                currentProgress += 0.1;
            }
            
            // 确保不超过95%（保留最后的5%用于实际完成）
            if (currentProgress > 95) {
                currentProgress = 95;
                clearInterval(progressInterval);
            }
            
            // 更新UI
            updateProgressUI(currentProgress);
        }, 100);
    }
    
    // 更新进度条UI
    function updateProgressUI(progress) {
        // 更新进度条填充
        progressBarFill.style.width = `${progress}%`;
        progressPercentage.textContent = `${Math.round(progress)}%`;
        
        // 估算tokens
        estimatedTokens = Math.round((progress / 100) * totalTokensEstimate);
        progressTokens.textContent = `${estimatedTokens} tokens`;
    }
    
    // 完成进度条
    function completeProgress() {
        // 清除计时器
        if (progressInterval) {
            clearInterval(progressInterval);
        }
        
        // 立即设置为100%
        currentProgress = 100;
        updateProgressUI(currentProgress);
        
        // 短暂延迟后隐藏进度条
        setTimeout(() => {
            progressContainer.classList.remove('active');
        }, 1000);
    }
    
    // Model selection change event
    modelSelect.addEventListener('change', function() {
        console.log(`模型已切换为: ${modelSelect.value}`);
        // Display notification
        const notification = document.getElementById('model-notification');
        if (notification) {
            notification.textContent = `当前选择模型: ${modelSelect.value}`;
            notification.style.opacity = '1';
            setTimeout(() => {
                notification.style.opacity = '0';
            }, 3000);
        }
    });
    
    // File upload handling
    csvFileInput.addEventListener('change', function(event) {
        const fileName = event.target.files[0]?.name || '拖放或点击上传文件';
        fileNameDisplay.textContent = fileName;
        
        // Check file extension
        if (event.target.files[0]) {
            const fileExt = fileName.split('.').pop().toLowerCase();
            const supportedExts = ['csv', 'xlsx', 'xls', 'json', 'parquet', 'feather', 'pickle', 'pkl'];
            
            if (!supportedExts.includes(fileExt)) {
                errorMessage.textContent = `警告: 文件格式 .${fileExt} 可能不被支持。支持的格式: ${supportedExts.join(', ')}`;
            } else {
                errorMessage.textContent = '';
            }
        }
    });
    
    // Handle file drag and drop
    const fileUploadWrapper = document.querySelector('.file-upload-wrapper');
    
    fileUploadWrapper.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = '#4285f4';
        this.style.backgroundColor = '#f8faff';
    });
    
    fileUploadWrapper.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.borderColor = '';
        this.style.backgroundColor = '';
    });
    
    fileUploadWrapper.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = '';
        this.style.backgroundColor = '';
        
        if (e.dataTransfer.files.length) {
            csvFileInput.files = e.dataTransfer.files;
            const fileName = e.dataTransfer.files[0]?.name || '拖放或点击上传文件';
            fileNameDisplay.textContent = fileName;
            
            // Check file extension
            const fileExt = fileName.split('.').pop().toLowerCase();
            const supportedExts = ['csv', 'xlsx', 'xls', 'json', 'parquet', 'feather', 'pickle', 'pkl'];
            
            if (!supportedExts.includes(fileExt)) {
                errorMessage.textContent = `警告: 文件格式 .${fileExt} 可能不被支持。支持的格式: ${supportedExts.join(', ')}`;
            } else {
                errorMessage.textContent = '';
            }
        }
    });
    
    // Generate code
    generateForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Clear previous output
        errorMessage.textContent = '';
        
        // Update UI to show loading state
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 生成中...';
        codeOutput.textContent = '# 正在生成代码，请稍候...';
        hljs.highlightElement(codeOutput);
        
        // 开始进度条动画
        startProgressAnimation();
        
        // Prepare form data
        const formData = new FormData();
        formData.append('model', modelSelect.value);
        formData.append('query', queryInput.value);
        
        if (csvFileInput.files.length > 0) {
            formData.append('csv_file', csvFileInput.files[0]);
        }
        
        // Send request
        fetch('/generate', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Reset button state
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-code"></i> 生成代码';
            
            // 完成进度条
            completeProgress();
            
            if (data.error) {
                // Show error
                errorMessage.textContent = data.error;
                codeOutput.textContent = '# 生成代码时出错';
                hljs.highlightElement(codeOutput);
                copyBtn.disabled = true;
            } else {
                // Show code
                codeOutput.textContent = data.code || '# 没有生成代码';
                hljs.highlightElement(codeOutput);
                copyBtn.disabled = !data.code;
                
                // 更新真实的 token 数量（如果后端提供）
                if (data.tokens) {
                    progressTokens.textContent = `${data.tokens} tokens`;
                }
            }
            
            // Refresh history
            loadHistory();
        })
        .catch(error => {
            // Reset button state
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-code"></i> 生成代码';
            
            // 完成进度条（出错）
            completeProgress();
            
            // Show error
            errorMessage.textContent = '请求失败: ' + error.message;
            codeOutput.textContent = '# 发送请求时出错';
            hljs.highlightElement(codeOutput);
            copyBtn.disabled = true;
        });
    });
    
    // Clear form
    clearBtn.addEventListener('click', function() {
        queryInput.value = '';
        csvFileInput.value = '';
        fileNameDisplay.textContent = '拖放或点击上传文件';
        codeOutput.textContent = '# 代码将在这里显示';
        hljs.highlightElement(codeOutput);
        errorMessage.textContent = '';
        copyBtn.disabled = true;
        progressContainer.classList.remove('active');
    });
    
    // 显示复制成功通知
    function showCopyNotification() {
        // 更改按钮文本和图标
        copyBtn.innerHTML = '<i class="fas fa-check"></i> 已复制';
        
        // 显示通知
        copyNotification.classList.add('show');
        
        // 添加脉冲效果
        copyBtn.style.animation = 'pulse 1s';
        
        // 2秒后隐藏通知和恢复按钮文本
        setTimeout(() => {
            copyNotification.classList.remove('show');
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> 复制代码';
            copyBtn.style.animation = '';
        }, 2000);
    }
    
    // Copy code
    copyBtn.addEventListener('click', function() {
        navigator.clipboard.writeText(codeOutput.textContent)
            .then(() => {
                showCopyNotification();
            })
            .catch(err => {
                console.error('复制失败:', err);
            });
    });
    
    // Clear history
    clearHistoryBtn.addEventListener('click', function() {
        fetch('/clear_history', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                historyList.innerHTML = '';
            }
        })
        .catch(error => {
            console.error('清除历史失败:', error);
        });
    });
    
    // Load history
    function loadHistory() {
        fetch('/history')
            .then(response => response.json())
            .then(data => {
                historyList.innerHTML = '';
                
                if (data.length === 0) {
                    historyList.innerHTML = '<div class="no-history">暂无历史记录</div>';
                    return;
                }
                
                data.forEach(item => {
                    const historyItem = document.createElement('div');
                    historyItem.className = 'history-item';
                    historyItem.addEventListener('click', () => {
                        // Populate form with history item
                        modelSelect.value = item.model;
                        queryInput.value = item.query;
                        
                        // Show code
                        codeOutput.textContent = item.code || '# 没有生成代码';
                        hljs.highlightElement(codeOutput);
                        copyBtn.disabled = !item.code;
                        errorMessage.textContent = '';
                    });
                    
                    // Format date
                    const date = new Date(item.timestamp);
                    const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
                    
                    historyItem.innerHTML = `
                        <div class="history-meta">
                            <span>${formattedDate}</span>
                            <span class="history-model">${item.model}</span>
                        </div>
                        <div class="history-query">${item.query}</div>
                        <div class="history-file">${item.file ? `文件: ${item.file}` : '示例数据'}</div>
                    `;
                    
                    historyList.appendChild(historyItem);
                });
            })
            .catch(error => {
                console.error('加载历史失败:', error);
                historyList.innerHTML = '<div class="load-error">加载历史记录失败</div>';
            });
    }
}); 