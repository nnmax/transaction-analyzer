const fs = require('fs');
const path = require('path');
const readline = require('readline');

// 查找当前目录的第一个 .txt 文件
const files = fs.readdirSync('./');
const txtFile = files.find(file => file.endsWith('.txt'));
if (!txtFile) {
    console.error('未找到 .txt 文件');
    process.exit(1);
}
const fileStream = fs.createReadStream(txtFile);

/**
 * 统计借方笔数和贷方笔数
*/
async function countLinesWithNumber() {
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    let count1 = 0;
    let count2 = 0

    for await (const line of rl) {
        const parts = line.split('|');
        if (parts.length > 8) {
            const num1 = Number.parseFloat(parts[7].trim().replace(',', ''));
            const num2 = Number.parseFloat(parts[8].trim().replace(',', ''));
            if (!Number.isNaN(num1)) count1++;
            if (!Number.isNaN(num2)) count2++;
        }
    }

    rl.close()

    console.log(`借方笔数: ${count1.toLocaleString()}; 贷方笔数: ${count2.toLocaleString()}`);
}

countLinesWithNumber();

/**
 * 统计借方合记或贷方合记
 */
async function sumNumbersAfterKeyword() {
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    let totalSum1 = 0;
    let totalSum2 = 0;

    for await (const line of rl) {
        const type1 = '借方合计'
        const type2 = '贷方合计'
        const index1 = line.indexOf(type1);
        const index2 = line.indexOf(type2);

        if (index1 !== -1) {
            const numberPart = line.substring(index1 + type1.length).trim().replaceAll(',', '');
            const number = parseFloat(numberPart);
            if (!isNaN(number)) totalSum1 += number;
        }

        if (index2 !== -1) {
            const numberPart = line.substring(index2 + type2.length).trim().replaceAll(',', '');
            const number = parseFloat(numberPart);
            if (!isNaN(number)) totalSum2 += number;
        }
    }

    rl.close()

    console.log(`借方合记: ${totalSum1.toLocaleString()}; 贷方合记: ${totalSum2.toLocaleString()}`);
}

sumNumbersAfterKeyword();

/**
 * 读取 a.txt，统计交易类型为「实时缴税」的笔数与借方发生额合计
 */
async function countRealtimeTaxFromA() {
    const filePath = path.join(__dirname, 'a.txt');
    const stream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: stream,
        crlfDelay: Infinity
    });

    let count = 0;
    let debitSum = 0;

    for await (const line of rl) {
        const parts = line.split('|');
        if (parts.length <= 8) continue;
        if (parts[4].trim() !== '实时缴税') continue;

        count++;
        const debit = Number.parseFloat(parts[7].trim().replaceAll(',', ''));
        if (!Number.isNaN(debit)) debitSum += debit;
    }

    rl.close();

    console.log(
        `实时缴税笔数: ${count.toLocaleString()}; 借方发生额合计: ${debitSum.toLocaleString()}`
    );
}

countRealtimeTaxFromA();
