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
    console.log(personSegmentation);
    if (!fs.existsSync(outputDir)) {
        await fs.mkdirSync(outputDir);
    }
    const imgBasename = path.basename(imagePath, '.jpg')
    const jsonName = imgBasename + '.json'
    await fs.promises.writeFile(outputDir + '/' + jsonName, JSON.stringify(personSegmentation));
}

async function walkDir(basePath, outputDir) {
    const net = await loadMode();
    const dirlist = fs.readdirSync(basePath);
    dirlist.forEach(function (dirname) {
        const new_path = basePath + "/" + dirname;
        main(net, new_path, outputDir);
    });
}

walkDir('demo_bodypix/jpg', 'demo_bodypix/output');

// main('./images/kids.jpg', 'output');