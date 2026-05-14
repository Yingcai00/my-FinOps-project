// 修复assetData数组位置的脚本
const fs = require('fs');

// 读取HTML文件
const htmlContent = fs.readFileSync('asset-ledger-management.html', 'utf-8');

// 找到assetData数组的开始位置
const assetDataStart = htmlContent.indexOf('const assetData = [');
if (assetDataStart === -1) {
    console.log('未找到assetData开始标记');
    process.exit(1);
}

// 找到assetData数组的结束位置
// 找到subdivideData数组的开始位置
const subdivideMarker = 'const subdivideData = [';
const subdivideIdx = htmlContent.indexOf(subdivideMarker, assetDataStart);
if (subdivideIdx === -1) {
    console.log('未找到subdivideData开始标记');
    process.exit(1);
}

// 从subdivideIdx向前查找];
let assetDataEnd = -1;
for (let i = subdivideIdx; i > assetDataStart; i--) {
    if (htmlContent.substring(i, i + 2) === '];') {
        assetDataEnd = i + 2;
        break;
    }
}

if (assetDataEnd === -1) {
    console.log('未找到assetData数组的结束位置');
    process.exit(1);
}

// 提取assetData数组
const assetData = htmlContent.substring(assetDataStart, assetDataEnd);

// 找到filteredAssetData初始化的位置
const filteredAssetDataStart = htmlContent.indexOf('let filteredAssetData = [...assetData];');
if (filteredAssetDataStart === -1) {
    console.log('未找到filteredAssetData初始化位置');
    process.exit(1);
}

// 找到filteredAssetData初始化之前的位置
// 找到"// 资产列表相关变量"这一行
const assetListVars = htmlContent.indexOf('// 资产列表相关变量', 0, filteredAssetDataStart);
if (assetListVars === -1) {
    console.log('未找到资产列表相关变量标记');
    process.exit(1);
}

// 构建新的HTML内容
// 1. 保留从开始到资产列表相关变量之前的内容
// 2. 插入assetData数组
// 3. 保留从资产列表相关变量到assetData数组开始之前的内容
// 4. 保留从assetData数组结束之后到文件结束的内容

const newHtml = 
    htmlContent.substring(0, assetListVars) + 
    assetData + '\n\n' + 
    htmlContent.substring(assetListVars, assetDataStart) + 
    htmlContent.substring(assetDataEnd);

// 保存更新后的HTML文件
fs.writeFileSync('asset-ledger-management.html', newHtml, 'utf-8');

console.log('HTML文件已更新，assetData数组已移到正确位置');
