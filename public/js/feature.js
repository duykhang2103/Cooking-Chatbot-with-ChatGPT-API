let card = document.querySelector('.card');
let cardHeader = document.querySelector('.card-header');
let cardBody = document.querySelector('.card-body');
let formOutline = document.querySelector('.form-outline');
let formControl = document.querySelector('.form-control');

function toggleCard(){
    card.classList.toggle('toggle-bubble');
    cardBody.classList.toggle('toggle-up');
    formOutline.classList.toggle('disappear');
    cardHeader.classList.toggle('toggle-header');
    document.querySelector('.title').classList.toggle('disappear');
    document.querySelector('.bubble-avatar').classList.toggle('appear');
}

let talking = false;
function turnOnSpeaker(){
    document.querySelector('.speaker').classList.toggle('speaker-on');
    if(talking == false) 
        talking = true;
    else
        talking = false;
}

function speak(speech) {
    if ('speechSynthesis' in window && talking) {
        var utterance = new SpeechSynthesisUtterance(speech);
        //msg.voice = voices[10]; // Note: some voices don't support altering params
        //msg.voiceURI = 'native';
        //utterance.volume = 1; // 0 to 1
        utterance.rate = 1.5; // 0.1 to 10
        //utterance.pitch = 1; //0 to 2
        //utterance.text = 'Hello World';
        //utterance.lang = 'en-US';
        speechSynthesis.speak(utterance);
    }
}

// SpeechRecognition section
let recognizing;
const speechRecog = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = new speechRecog();

// So sad that SpeechRecognition doesn't work on Opera :(

// console.log(new speechRecog());
  
recognition.continuous = true;
reset();
recognition.onend = reset;

recognition.onresult = (event) => {
    for (var i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
        formControl.value += event.results[i][0].transcript;
        }
    }
}

function reset() {
    recognizing = false;
    document.querySelector('.mic').classList.remove('mic-on');
}

function turnOnMic(){
    document.querySelector('.mic').classList.add('mic-on');
    if (recognizing) {
        recognition.stop();
        reset();
    } else {
        recognition.start();
        recognizing = true;
    }
}