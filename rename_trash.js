const fs = require('fs');
const path = require('path');

const docsDir = 'd:/documents/docs';
const targets = ['intro.md', 'tutorial-basics', 'tutorial-extras'];

targets.forEach(target => {
    const oldPath = path.join(docsDir, target);
    const newPath = path.join(docsDir, '_' + target);
    
    if (fs.existsSync(oldPath)) {
        try {
            fs.renameSync(oldPath, newPath);
            console.log(`Renamed ${target} to _${target}`);
        } catch (err) {
            console.error(`Failed to rename ${target}: ${err.message}`);
            // Try to set draft: true for markdown files inside folders as backup
            if (fs.lstatSync(oldPath).isDirectory()) {
                console.log(`Attempting to hide contents of ${target}...`);
                 // (Simplified: just ignore for now, rename log is consistent)
            }
        }
    } else {
        console.log(`${target} not found`);
    }
});
