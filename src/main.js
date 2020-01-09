// 使用@tensorflow/tfjs-node加速，同时有GPU版本@tensorflow/tfjs-node-gpu
// 可以只使用@tensorflow/tfjs-node-gpu，当没有GPU时会自动回退使用CPU
const tfjs = require('@tensorflow/tfjs-node-gpu');
const bodyPix = require('@tensorflow-models/body-pix');
const fs = require('fs');
const path = require('path');
var jpeg = require('jpeg-js');

async function loadMode() {
    const net = await bodyPix.load({
        architecture: "ResNet50",
        quantBytes: 1,
        outputStride: 16,
        modelUrl: "http://172.20.121.19:8000/ResNet50/model-stride16.json"
    });
    return net;
}

async function loadImageManual(path) {
    console.log('loadImageManual decoding ' + path)
    const jpegData = fs.readFileSync(path);
    const pixels = jpeg.decode(jpegData, true);

    const numChannels = 3;
    const numPixels = pixels.width * pixels.height;
    const values = new Int32Array(numPixels * numChannels);

    for (let i = 0; i < numPixels; i++) {
        for (let channel = 0; channel < numChannels; ++channel) {
            values[i * numChannels + channel] = pixels[i * 4 + channel];
        }
    }

    // fill pixels with pixel channel bytes from image
    const outShape = [pixels.height, pixels.width, numChannels];
    const input = tfjs.tensor3d(values, outShape, 'int32');
    console.log('loadImageManual decoded')
    return input;
}

async function loadImageManual(path) {
    const file = await fs.promises.readFile(path);
    console.log('decoding ' + path)
    const image = await tfjs.node.decodeImage(file, 3);
    console.log('decoded')
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
    console.log('personSegmentation')
    const personSegmentation = await net.segmentPersonParts(image);
    console.log('personSegmentation done')
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
        console.log("process file: " + jpgName);
        const jpg_path = path.join(jpgDir, jpgName);
        await main(net, jpg_path, outputJsonDir);
    }
}

if (process.argv.length <= 2) {
    console.error(`Need run with: ${path.basename(process.argv[1])} <dir>`)
} else {
    root_dir = path.resolve(process.argv[2])
    walkDir(root_dir)
}

// const net = loadMode();
// main(net, '../images/kids.jpg', '../output');