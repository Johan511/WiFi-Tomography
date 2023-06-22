//CS21B033
const express = require("express")
const fs = require("fs")
const bodyParser = require("body-parser")
const REC_FILENAME = "receiver.csv"
const TRANS_FILENAME = "transmitter.csv"


function choose_image(dir = "images") {
    let images = []
    fs.readdirSync(dir).forEach(f => images.push(f))


    filteredImages = images.filter(f => f.length == "fig10.png".length)
    console.log(filteredImages)

    return filteredImages[filteredImages.length - 1]
}


const app = express()
var options = {
    inflate: true,
    limit: '100kb',
};

app.use(function (req, res, next) {
    var data = '';
    req.setEncoding('utf8');
    req.on('data', function (chunk) {
        data += chunk;
    });

    req.on('end', function () {
        req.body = data;
        next();
    });
});
app.post("/rec", (req, res) => {
    console.log(req.body)
    console.log(req.query)
    // fs.writeFileSync("file.txt", 'Text', "UTF-8",{'flags': 'w+'});
    fs.appendFileSync(REC_FILENAME, `${req.query["lat"]},${req.query["longitude"]},${req.query["time"]},${req.body}\n`, { 'flags': 'a' })
})

app.post("/TRANS", (req, res) => {
    console.log(req.body)
    console.log(req.query)
    fs.appendFileSync(TRANS_FILENAME, `${req.query["lat"]},${req.query["longitude"]},${req.query["time"]},${req.body}\n`, { 'flags': 'a' })
})

app.get("/map", (req, res) => {
    lastest_img_name = choose_image()

    fs.createReadStream("images/" + lastest_img_name).pipe(res);

})

app.listen(8000, () => { console.log("listening to 8000") })
