class InteractiveChatbox {
    constructor(a, b, c) {
        this.args = {
            button: a,
            chatbox: b
        }
        this.icons = c;
        this.state = false; 
    }

    display() {
        const {button, chatbox} = this.args;
        
        button.addEventListener('click', () => this.toggleState(chatbox))
    }

    toggleState(chatbox) {
        this.state = !this.state;
        this.showOrHideChatBox(chatbox, this.args.button);
    }

    showOrHideChatBox(chatbox, button) {
        if(this.state) {
            chatbox.classList.add('chatbox--active')
            this.toggleIcon(true, button);
        } else if (!this.state) {
            chatbox.classList.remove('chatbox--active')
            this.toggleIcon(false, button);
        }
    }

    toggleIcon(state, button) {
        const { isClicked, isNotClicked } = this.icons;
        let b = button.children[0].innerHTML;

        if(state) {
            button.children[0].innerHTML = isClicked; 
        } else if(!state) {
            button.children[0].innerHTML = isNotClicked;
        }
    }
    displayMessage(message,messageInput,messageBox,sender){
        console.log(message)
        if (sender=="guest"){
            const messageNode = this.stringToHTML(`<div class="messages__item messages__item--operator">${message}</div>`)
            messageBox.appendChild(messageNode)

        }
        else if (sender=='robot'){
            const messageNode = this.stringToHTML(`<div class="messages__item messages__item--visitor">${message}</div>`);
            messageBox.appendChild(messageNode)

        }
        else{
            const messageNode = this.stringToHTML(`<div class="messages__item messages__item--typing">
            <span class="messages__dot"></span>
            <span class="messages__dot"></span>
            <span class="messages__dot"></span>
    </div>`);
            messageBox.appendChild(messageNode)
            
        }
        messageInput.value = ''
    }

     stringToHTML(str) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(str, 'text/html');
        return doc.querySelector('div');
    };
}