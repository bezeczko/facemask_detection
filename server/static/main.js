//peer connection
var pc = null;

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
    document.getElementById('start').style.display = 'none';

    pc = createPeerConnection();

    var constraints = {
        audio: false,
        video: true
    }

    document.getElementById('video').style.display = 'block';

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        stream.getTracks().forEach(function(track) {
            pc.addTrack(track, stream);
        });
        return negotiate();
    }, function(err) {
        alert('Could not acquire media: ' + err);
    });

    document.getElementById('stop').style.display = 'inline-block';
}

function stop() {
    document.getElementById('stop').style.display = 'none';

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

    document.getElementById('start').style.display = 'inline-block';
    document.getElementById('video').style.display = 'none';
}
