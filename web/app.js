// DocFlow AI Web UI JavaScript

const API_BASE_URL = 'http://localhost:8000/api/v1';

// 文件选择处理
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    fileInput.files = e.dataTransfer.files;
});

// 处理文档
async function processDocuments() {
    const files = fileInput.files;
    if (files.length === 0) {
        alert('请选择至少一个文件');
        return;
    }

    const enableValidation = document.getElementById('enableValidation').checked;
    const documentType = document.getElementById('documentType').value;

    // 显示状态区域
    document.getElementById('statusSection').style.display = 'block';
    document.getElementById('progressFill').style.width = '0%';
    document.getElementById('statusText').textContent = '正在上传文件...';

    try {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        // 模拟处理进度
        simulateProgress();

        // 调用 API（实际使用时取消注释）
        // const response = await fetch(`${API_BASE_URL}/documents/process`, {
        //     method: 'POST',
        //     body: formData
        // });
        // const result = await response.json();

        // 模拟响应
        setTimeout(() => {
            document.getElementById('progressFill').style.width = '100%';
            document.getElementById('statusText').textContent = '处理完成！';
            
            showResults({
                document_id: `doc_${Date.now()}`,
                status: 'completed',
                extracted_fields: {
                    party_a: '示例公司 A',
                    party_b: '示例公司 B',
                    amount: '100,000.00 CNY'
                },
                validation_report: {
                    is_valid: true,
                    total_rules_checked: 10,
                    reasoning_chain_length: 10
                },
                processing_time: 8.2
            });
        }, 2000);

    } catch (error) {
        alert(`处理失败：${error.message}`);
        document.getElementById('statusText').textContent = '处理失败';
    }
}

// 模拟进度条
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
        }
        document.getElementById('progressFill').style.width = `${progress}%`;
        
        const stages = ['上传中...', '文档分析...', '信息抽取...', '逻辑验证...', '生成报告...'];
        const stageIndex = Math.min(Math.floor(progress / 20), stages.length - 1);
        document.getElementById('statusText').textContent = stages[stageIndex];
    }, 400);
}

// 显示结果
function showResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsSection.style.display = 'block';
    
    resultsContent.innerHTML = `
        <div class="result-card">
            <h3>✅ 处理成功</h3>
            <p><strong>文档 ID:</strong> ${result.document_id}</p>
            <p><strong>处理时间:</strong> ${result.processing_time.toFixed(2)}秒</p>
            
            <h4>提取的字段:</h4>
            <pre>${JSON.stringify(result.extracted_fields, null, 2)}</pre>
            
            <h4>验证报告:</h4>
            <p>验证状态：${result.validation_report.is_valid ? '✅ 通过' : '❌ 未通过'}</p>
            <p>检查规则数：${result.validation_report.total_rules_checked}</p>
            <p>推理链长度：${result.validation_report.reasoning_chain_length}步</p>
        </div>
    `;
    
    // 滚动到结果区域
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// 加载系统统计
async function loadStats() {
    try {
        // const response = await fetch(`${API_BASE_URL}/stats`);
        // const stats = await response.json();
        
        // 使用示例数据
        const stats = {
            total_documents_processed: 12000,
            average_processing_time: 8.0,
            accuracy_rate: 0.96
        };
        
        console.log('系统统计:', stats);
    } catch (error) {
        console.error('加载统计失败:', error);
    }
}

// 页面加载时获取统计
window.addEventListener('load', loadStats);
