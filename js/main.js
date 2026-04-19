// 段永平知识库 - JavaScript

// 全局数据
let allData = {
    companies: [],
    topics: [],
    quotes: []
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    loadData();
});

// 加载数据
async function loadData() {
    try {
        // 从分析结果加载
        const response = await fetch('data/analysis.json');
        const data = await response.json();

        // 转换公司数据
        allData.companies = Object.entries(data.top_companies).map(([name, pages]) => ({
            name,
            mentions: pages.length,
            pages
        }));

        // 转换主题数据
        allData.topics = Object.entries(data.topics).map(([name, pages]) => ({
            name,
            mentions: pages.length,
            pages
        }));

        // 加载语录
        allData.quotes = data.quotes;

    } catch (error) {
        console.error('加载数据失败:', error);
    }
}

// 搜索功能
function search(query, type) {
    query = query.toLowerCase();
    const results = allData[type].filter(item => {
        if (type === 'quotes') {
            return item.text.toLowerCase().includes(query);
        }
        return item.name.toLowerCase().includes(query);
    });
    return results;
}

// 过滤器
function filterByTopic(quotes, topic) {
    if (!topic || topic === 'all') return quotes;
    return quotes.filter(q => q.topics && q.topics.includes(topic));
}

// 排序
function sortBy(field) {
    return function(a, b) {
        return b[field] - a[field];
    };
}

// 格式化数字
function formatNumber(num) {
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k';
    }
    return num.toString();
}

// 显示提示
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #1a365d;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// 导出数据为JSON
function exportData() {
    const dataStr = JSON.stringify(allData, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'duanyongping_knowledge.json';
    a.click();
}
