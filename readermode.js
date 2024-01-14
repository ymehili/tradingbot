const { Readability } = require('@mozilla/readability');
const { JSDOM } = require('jsdom');
const fs = require('fs');
const argv = process.argv;

const filePath = argv[2];

function putinreadermode(dom) {
    var article = new Readability(dom.window.document).parse();
    var content = 'Title: ${article.title} \n\n ${article.content}';
    fs.writeFile('output.txt', content, (err) => {
        if (err)
            throw err;
        console.log('The file has been saved!');
    });
    console.log(article);
}

function main() {
    fs.readFile(filePath, 'utf8', (err, html) => {
        if (err) {
            throw err;
        }

        const dom = new JSDOM(html);
        putinreadermode(dom);
    });
}

main();