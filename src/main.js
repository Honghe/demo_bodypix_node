// 使用@tensorflow/tfjs-node加速，同时有GPU版本
const tfjs = require('@tensorflow/tfjs-node');
const bodyPix = require('@tensorflow-models/body-pix');
const fs = require('fs');
const path = require('path');

async function loadMode() {
    const net = await bodyPix.load({
        architecture: "ResNet50",
        quantBytes: 1,
        outputStride: 16,
        modelUrl: "http://0.0.0.0:8000/ResNet50/model-stride16.json"
    });
    return net;
}


async function loadImage(path) {
    const file = await fs.promises.readFile(path);
    const image = await tfjs.node.decodeImage(file, 3);
    return image;
}

async function main(net, imagePath, outputDir) {
    const image = await loadImage(imagePath);

    /**
     * One of:
     *   - net.segmentPerson
     *   - net.segmentPersonParts
     *   - net.segmentMultiPerson
     *   - net.segmentMultiPersonParts
     * See documentation below for details on each method.
     */
    const personSegmentation = await net.segmentPersonParts(image, {});
    // console.log(personSegmentation);
    if (!fs.existsSync(outputDir)) {
        await fs.mkdirSync(outputDir);
    }
    const imgBasename = path.basename(imagePath, '.jpg')
    const jsonName = imgBasename + '.json'
    await fs.promises.writeFile(outputDir + '/' + jsonName, JSON.stringify(personSegmentation));
}

async function walkDir(rootPath) {
    const jpgDir = path.join(rootPath, 'jpgs');
    const outputJsonDir = path.join(rootPath, 'jsons');
    const net = await loadMode();
    const dirlist = fs.readdirSync(jpgDir);
    for (const jpgName of dirlist) {
        console.log("process file: " + jpgName)
        const jpg_path = jpgDir + "/" + jpgName;
        await main(net, jpg_path, outputJsonDir);
    }
}

if (process.argv.length <= 2) {
    console.error(`Need run with: ${path.basename(process.argv[1])} <dir>`)
} else {
    root_dir = path.resolve(process.argv[2])
    walkDir(root_dir)
}

// main('./images/kids.jpg', 'output');