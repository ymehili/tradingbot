const { Readability } = require('@mozilla/readability');
const { JSDOM } = require('jsdom');

const filePath = argv[2];

fs.readFile(filePath, 'utf8', (err, html) => {
    if (err) {
        throw err;
    }

    const dom = new JSDOM(html);
    console.log(dom.window.document.querySelector("body").textContent);
});

