$(document).ready(function(){

    $("#but_upload").click(function(){

        var fd = new FormData();
        var files = $('#file')[0].files;
        

        if(files.length > 0 ){
        fd.append('file',files[0]);

        $.ajax({
            url: 'http://127.0.0.1:8000/image/',
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            success: function(response){
             if(response != 0){
                
                console.log(response["name"])
                
                if(response["suffix"] == "mp4") {
                    $("#my-video source").attr("src","../backend/Images/"+response["name"]+"."+response["suffix"]);
                    $("#my-video")[0].load()
                    $("#my-video").show();
                } else {
                    $("#img").attr("src","../backend/Images/"+response["name"]+"."+response["suffix"]); 
                    $(".preview img").show();
                }


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

$("#image-btn").click(function() {
    $(".image-container").show();
    $(".webcam-container").hide();
});

$("#webcam-btn").click(function() {
    $(".image-container").hide();
    $(".webcam-container").show();
});