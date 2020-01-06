// 使用@tensorflow/tfjs-node加速，同时有GPU版本
const tfjs = require('@tensorflow/tfjs-node');
const bodyPix = require('@tensorflow-models/body-pix');
const fs = require('fs');

async function loadImage(path) {
    const file = await fs.promises.readFile(path);
    const image = await tfjs.node.decodeImage(file, 3);
    return image;
}

async function main() {
    const image = await loadImage('./images/kids.jpg');
    const net = await bodyPix.load({
        architecture: "ResNet50",
        quantBytes: 1,
        outputStride: 16,
        modelUrl: "http://0.0.0.0:8000/ResNet50/model-stride16.json"
    });

    /**
     * One of:
     *   - net.segmentPerson
     *   - net.segmentPersonParts
     *   - net.segmentMultiPerson
     *   - net.segmentMultiPersonParts
     * See documentation below for details on each method.
     */
    const personSegmentation = await net.segmentPersonParts(image, {
    });
    console.log(personSegmentation);
    const dir = 'output';
    if (!fs.existsSync(dir)){
        await fs.mkdirSync(dir);
    }
    await fs.promises.writeFile(dir + '/segs.json', JSON.stringify(personSegmentation));
}

main();