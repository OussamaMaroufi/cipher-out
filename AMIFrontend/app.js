const chatButton = document.querySelector('.chatbox__button');
const chatContent = document.querySelector('.chatbox__support');
const sendButton = document.querySelector(".chatbox__send--footer")
const messageInput = document.querySelector('.chatbox__footer input')
const messageBox = document.querySelector('.chatbox__messages div')
const icons = {
    isClicked: '<img src="./images/icons/chatbox-icon.svg" />',
    isNotClicked: '<img src="./images/icons/chatbox-icon.svg" />'
}
const chatbox = new InteractiveChatbox(chatButton, chatContent, icons,sendButton,messageInput,messageBox,);
chatbox.display();
chatbox.toggleIcon(false, chatButton);


function insertIntoMessageBox(message,sender){
    if (message.length > 0){
        chatbox.displayMessage(message,messageInput,messageBox,sender);
        
    }



}


sendButton.addEventListener('click',(event)=> {
        mess = messageInput.value
        if(mess.length > 0){
        insertIntoMessageBox(mess,"guest");
        postData("http://localhost:8000/api/v1/sendmsg/",data={
            'body':mess
        })
        .then(data => {
            console.log(data)
            insertIntoMessageBox(data[data.length-1].result,"robot")
          }).catch((err=>{
            console.log(err)
          }));

        }});

messageInput.addEventListener('keyup',(event)=>{
    if (event.code == 'Enter'){
        mess = event.target.value
        insertIntoMessageBox(event.target.value,"guest");
        postData("http://localhost:8000/api/v1/sendmsg/",data={
            'body':mess
        })
        .then(data => {
            console.log(data)
            insertIntoMessageBox(data[data.length-1].result,"robot")
          }).catch((err=>{
            console.log(err)
          }));

    }
})

function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }
  

async function postData(url = '',data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/json'
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
      body: JSON.stringify(data) // body data type must match "Content-Type" header

    });
    return response.json(); // parses JSON response into native JavaScript objects
  }
  
function getClientPosition()  {
     
    if ("geolocation" in navigator) {
        // check if geolocation is supported/enabled on current browser
         navigator.geolocation.getCurrentPosition(
         function success(position) {
           // for when getting location is a success
         window.$pos  = {'latitude': position.coords.latitude, 
                       'longitude': position.coords.longitude};
         },
        function error(error_message) {
          // for when getting location results in an error
          console.error('An error has occured while retrieving location', error_message)
        }
        
    );
}
      else {
        // geolocation is not supported
        // get your location some other way
        console.log('geolocation is not enabled on this browser');
      }

      
}


async function getPositionByAddress(address){
    let response = await fetch("https://atlas.microsoft.com/search/address/json?api-version=1.0&query="+address+"&subscription-key=tdRchAxxx6a7U8zu5O5KR13-79_VtzKAtzJOQ-6yBZs&routeType=shortest",
    {
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*'
        }
            })
    let data = await response.json();
    console.log(data)
}


choices = document.querySelectorAll('.clickable_choice').forEach((el,key,parent)=>{
    el.addEventListener("click",(el)=>{
        console.log(el.target.innerText)
        if(el.target.innerText === "1- Questions generales"){
            insertIntoMessageBox("C'est quoi votre question?","robot");}
        else{
            insertIntoMessageBox("Veuillez attendre ...","robot");
            insertIntoMessageBox("PLease wait while we get you the nearest agencies ...","wait");
        }
    
    })
})