var recordButton, recorder;
var clicked = 0;
var data;
var localStream;
var context;
var i = 0;
var ctx = document.getElementById("myChart");

var myChart = new Chart(ctx, {
  type: 'line',
  data: {
  },
  options: {
    legend: {
      display: false
    },
    responsive: false,
    title: {
      display: true,
      text: "Input Volume and Corresponding Note"
    },
    scales: {
      xAxes: [
        {
          ticks: {
            display: false
          }
        }
      ],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'RMS * 100'
        }
      }]
    }
  }
});



function mainButton() {
  var mainButton = document.getElementById('mainButton');
  if(clicked == 0) {
    recordAudio();
    mainButton.innerText = "Stop Recording";
    clicked = 1;
  }
  else {
    stopStream();
    mainButton.innerText = "Record Audio";
    clicked = 0;
  }
}

//uses MediaRecorder API for recording and Web Audio API to get raw sound
//data. Sends raw audio data to server.
function recordAudio () {
  recordButton = document.getElementById('record');

  //Get permission to use computer microphone
  navigator.mediaDevices.getUserMedia({
    audio: true, video: false
  })
  .then(function (stream) {
    recorder = new MediaRecorder(stream);
    recorder.addEventListener('dataavailable', onFinishedRecording);
    recorder.start();

    localStream = stream.getTracks()[0];
    context = new AudioContext();
    var source = context.createMediaStreamSource(stream);
    var processor = context.createScriptProcessor(4096, 1, 1);

    source.connect(processor);
    processor.connect(context.destination);

    processor.onaudioprocess = function(e) {
      i = i+1;
      console.log(i);
      var fldata = e.inputBuffer.getChannelData(0);
      do_ajax(fldata);
    }
  });

};

//Stops the MediaRecorder recording, closes the web audio context, and then
//alerts the server that the recording has finished
function stopStream() {
  recorder.stop();
  console.log("Stopped");
  localStream.stop();
  context.close();
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (this.readyState==4 && this.status == 200) {
      var responseData = JSON.parse(this.responseText);
      document.getElementById("notesReturned").innerHTML = responseData.guitar_notes;
      console.log(responseData.rms_data)
      myChart.data.labels = responseData.note_list_data;
      myChart.data.datasets = [{
        data: responseData.rms_data,
        borderColor: "#3e95cd",
        fill: false
      }]
      myChart.update();
    }
  };
  req.open("POST","/index/", true);
  req.send("stop");
}

//sends data to Flask
function do_ajax(postData) {
  var req = new XMLHttpRequest();
  req.onreadystatechange = function() {
    if (this.readyState==4 && this.status == 200) {
      document.getElementById("new-text").innerHTML = this.responseText;
    }
  };
  req.open("POST", "/index/", true);
  req.send(postData);
}

//Recieves a "dataavailable" signal upon the recorder being stopped
//and then takes the recorded data and creates a URL object to store
//in the HTML audio element
function onFinishedRecording(e) {
  var audio = document.getElementById('player');
  data = e.data;
  audio.src = URL.createObjectURL(e.data);
  console.log(e.data);
}
