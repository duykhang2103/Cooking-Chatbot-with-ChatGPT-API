
function createMessage(data, user){
    let newMes = document.createElement('div');
    newMes.classList.add('message');
    newMes.classList.add('d-flex');
    newMes.classList.add('flex-row');
    newMes.classList.add('mb-4');
    
    let ava = document.createElement('img');
    let mes = document.createElement('div');
    let text = document.createElement('div');
    
    ava.alt="avatar";
    ava.style.width =  "45px"; 
    ava.style.height = "45px";
    ava.style.borderRadius = "50%";
    mes.classList.add("p-3");
    mes.style.borderRadius ="15px";

    text.classList.add("small");
    text.classList.add("mb-0");
    text.innerHTML = data;
    mes.appendChild(text);

    if(user == "AI") {
        newMes.classList.add('justify-content-start');
        ava.src = '../public/img/ai.png';
        mes.classList.add("ms-3");
        mes.style.backgroundColor = "rgba(57, 192, 237,.2)";
        newMes.appendChild(ava);
        newMes.appendChild(mes);
        speak(data);
    }
    else {
        newMes.classList.add('justify-content-end');
        ava.src = '../public/img/human.png';
        mes.classList.add("me-3");
        mes.classList.add("border");
        mes.style.backgroundColor = "rgba(237, 207, 57, 0.2)";
        newMes.appendChild(mes);
        newMes.appendChild(ava);
    }

    return newMes;
}

function handleSubmitEvent(event){
    
}


$(document).ready(function() {
    $('.form-outline').submit(function(event) {
        event.preventDefault(); // prevent the form from submitting normally

        let cardBody = document.querySelector('.card-body');
        let input_text = document.getElementById('textAreaExample').value;
        let newMessage = createMessage(input_text, "Human");

        cardBody.append(newMessage);
        cardBody.scrollTop = cardBody.scrollHeight;
        storeData(newMessage);

        document.getElementById('textAreaExample').value='';

        $.ajax({
            type: 'POST',
            url: '/',
            data: {'input_text': input_text},
            success: function(data) {
                let modText = data.output_text.replace(new RegExp('\r?\n','g'), '<br>');
                newMessage = createMessage(modText, "AI"); 
                cardBody.append(newMessage);
                cardBody.scrollTop = cardBody.scrollHeight;
                storeData(newMessage);
            }
        });
    });
});