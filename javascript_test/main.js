var fileTag = document.getElementById("file");
var image = document.getElementById("image");

fileTag.addEventListener("change", function() {
    processImage(this);
});

function processImage(input) {
    var reader;

    reader = new FileReader();
    reader.onload = function(e) {
        image.setAttribute("src", e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
}

function openCvReady() {
    cv['onRuntimeInitialized']=()=>{
        // do all your work here
        console.log("test");
        let canvasFrame = document.getElementById("canvasFrame"); // canvasFrame is the id of <canvas>
        let context = canvasFrame.getContext("2d");
        let src = new cv.Mat(480, 640, cv.CV_8UC4);
        let dst = new cv.Mat(480, 640, cv.CV_8UC1);
        const FPS = 30;

        function processVideo() {
            let begin = Date.now();
            context.drawImage(video, 0, 0, 640, 480);
            src.data.set(context.getImageData(0, 0, 640, 480).data);
            cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
            cv.imshow("canvasFrame", dst); // canvasOutput is the id of another <canvas>;
            // schedule next one.
            let delay = 1000/FPS - (Date.now() - begin);
            setTimeout(processVideo, delay);
        }

        // schedule first one.
        setTimeout(processVideo, 0);
    };
}