const fs = require('fs');
const path = require('path');

const targetDirs = [
    'd:/documents/docs/tutorial-basics',
    'd:/documents/docs/tutorial-extras'
];

targetDirs.forEach(dir => {
    if (fs.existsSync(dir)) {
        const files = fs.readdirSync(dir);
        files.forEach(file => {
            if (file.endsWith('.md')) {
                const filePath = path.join(dir, file);
                try {
                    const content = fs.readFileSync(filePath, 'utf8');
                    if (!content.includes('draft: true')) {
                        const newContent = "---\ndraft: true\n---\n" + content;
                        fs.writeFileSync(filePath, newContent);
                        console.log(`Hid ${file}`);
                    }
                } catch(e) {
                    console.error(`Error hiding ${file}: ${e.message}`);
                }
            }
        });
    }
});
