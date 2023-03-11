
// restoreData();
// clearData();
function restoreData(){
    let cardBody = document.querySelector('.card-body');
    
    for(let i = 0; i < localStorage.length; i++){
        let tempDiv = document.createElement('div');

        tempDiv.innerHTML = localStorage.getItem(`message${i}`);
        
        cardBody.append(tempDiv);
    }
    cardBody.scrollTop = cardBody.scrollHeight;
}

function storeData(message){
    localStorage.setItem(`message${localStorage.length++}`, message.outerHTML);
    // console.log(localStorage);
}

function clearData(){
    localStorage.clear();
    while(cardBody.firstChild){
        cardBody.removeChild(cardBody.firstChild);
    }
}