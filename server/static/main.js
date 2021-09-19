//peer connection
var pc = null;

var webcamContainer = document.getElementById("webcam-container");
var photoVideoContainer = document.getElementById("photovideo-container");
var photovideoBtn = document.getElementById("photovideoBtn");
var cameraBtn = document.getElementById("cameraBtn");

function createPeerConnection() {
    
    var config = {
        sdpSemantics: 'unified-plan'
    }

    pc = new RTCPeerConnection(config);

    pc.addEventListener('track', function(evt) {
        if (evt.track.kind == 'video')
            document.getElementById('camera-output').srcObject = evt.streams[0];
    });

    return pc;

}

function negotiate() {
    return pc.createOffer().then(function(offer) {
        return pc.setLocalDescription(offer);
    }).then(function() {
        //wait for ICE gathering to complete
        return new Promise(function(resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function() {
        var offer = pc.localDescription;
        var codec = 'default';
        return fetch('/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
                kind: "video"
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then(function(response) {
        return response.json();
    }).then(function(answer) {
        return pc.setRemoteDescription(JSON.parse(answer));
    }).catch(function(e) {
        alert(e);
    })
}

function start() {
    document.getElementById('start').hidden = true;

    pc = createPeerConnection();

    var constraints = {
        audio: false,
        video: {
            width: { min: 640, ideal: 1280, max: 1280 },
            height: { min: 480, ideal: 720, max: 720 }
        }
    }

    document.getElementById('video').hidden = false;

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        stream.getTracks().forEach(function(track) {
            pc.addTrack(track, stream);
        });
        return negotiate();
    }, function(err) {
        alert('Could not acquire media: ' + err);
    });

    document.getElementById('stop').hidden = false;
}

function stop() {
    document.getElementById('stop').hidden = true;

    if(pc.getTransceivers) {
        pc.getTransceivers().forEach(function(transceiver) {
            if(transceiver.stop) {
                transceiver.stop();
            }
        });
    }

    pc.getSenders().forEach(function(sender) {
        sender.track.stop();
    });

    setTimeout(function() {
        pc.close();
    }, 500);

    document.getElementById('start').hidden = false;
    document.getElementById('video').hidden = true;
}

function webcamClick() {
    if (webcamContainer.hidden == true) {
        photoVideoContainer.style.display = 'none';
        webcamContainer.hidden = false;
        cameraBtn.style.textDecoration = "underline"
        cameraBtn.style.fontWeight = "bold"
        photovideoBtn.style.textDecoration = "none"
        photovideoBtn.style.fontWeight = "normal"
    }
}

function photoVideoClick() {
    if (photoVideoContainer.style.display == 'none') {
        webcamContainer.hidden = true;
        photoVideoContainer.style.display = 'block';
        cameraBtn.style.textDecoration = "none"
        cameraBtn.style.fontWeight = "normal"
        photovideoBtn.style.textDecoration = "underline"
        photovideoBtn.style.fontWeight = "bold"
    }
}

$(document).ready(function(){

    $("#but_upload").click(function(){

        var fd = new FormData();
        var files = $('#file')[0].files;
        

        if(files.length > 0 ){
        fd.append('file',files[0]);

        $.ajax({
            url: 'http://127.0.0.1:8000/photovideo',
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            success: function(response){
             if(response != 0){
                
                console.log(response)

                $("#img").attr('src',`data:image/png;base64,${response["encoded_img"]}`);
                // let height = response["img_dimensions"].substring(1, response["img_dimensions"].length-1).split(',')[0];
                // let width = response["img_dimensions"].substring(1, response["img_dimensions"].length-1).split(',')[1];
                // console.log(width)
                // $("#img").height(height).width(width);
                
                // if(response["suffix"] == "mp4") {
                //     $("#my-video source").attr("src","../backend/Images/"+response["name"]+"."+response["suffix"]);
                //     $("#my-video")[0].load()
                //     $("#my-video").show();
                // } else {
                //     $("#img").attr("src","../backend/Images/"+response["name"]+"."+response["suffix"]); 
                //     $(".preview img").show();
                // }


             }else{
                alert('file not uploaded');
             }
          },
        });
        } else {
            alert("Please select a file.");
        }
    });
});