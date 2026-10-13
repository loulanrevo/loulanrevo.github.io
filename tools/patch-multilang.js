const fs = require('fs');
const path = require('path');

const targetFile = path.join(__dirname, '..', 'node_modules', 'hexo-multiple-language-generate', 'index.js');

if (fs.existsSync(targetFile)) {
    try {
        let content = fs.readFileSync(targetFile, 'utf8');
        const unquotedTarget = `runHexoCommand(args, workingDir) {\n        const command = this.resolveHexoCommand();`;
        const replacement = `runHexoCommand(args, workingDir) {\n        let command = this.resolveHexoCommand();\n        if (process.platform === 'win32' && !command.startsWith('"')) {\n            command = \`"\${command}"\`;\n        }`;

        if (content.includes(unquotedTarget)) {
            content = content.replace(unquotedTarget, replacement);
            fs.writeFileSync(targetFile, content, 'utf8');
            console.log('[patch] 成功修复 hexo-multiple-language-generate 在 Windows 带空格路径下的兼容性问题。');
        } else if (content.includes('if (process.platform === \'win32\' && !command.startsWith(\'"\'))')) {
            console.log('[patch] hexo-multiple-language-generate 已经是修复状态。');
        } else {
            console.log('[patch] 未找到待替换模式，跳过修补。');
        }
    } catch (err) {
        console.warn('[patch] 修补过程提示:', err.message);
    }
}
