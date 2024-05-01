document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.navbar-home a').addEventListener('mouseover', function() {
      this.style.transform = 'scale(1.1)';
    });
  
    document.querySelector('.navbar-home a').addEventListener('mouseout', function() {
      this.style.transform = 'scale(1)';
    });
  });
  

class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            chatMessages: document.querySelector('.chatbox__messages') // Reference to chat messages container
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const inputField = chatBox.querySelector('input');
        inputField.addEventListener("keyup", (event) => {
            if (event.key === "Enter") {
                this.onSendButton(chatBox);
            }
        });

        // Add event listener to clear chat on image click
        const clearButton = document.querySelector('.chatbox__button button');
        clearButton.addEventListener('click', () => this.clearChat());
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // Show or hide the chatbox
        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text1 = textField.value.trim(); // Trim the input text

        if (text1 === "") {
            return;
        }

        const msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);

        // Replace $SCRIPT_ROOT with the actual endpoint URL
        fetch("/predict", {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                const msg2 = { name: "Sam", message: data.answer };
                this.messages.push(msg2);
                this.updateChatText(chatbox);
                textField.value = ''; // Clear input field after sending message
            })
            .catch(error => {
                console.error('Error:', error);
                this.updateChatText(chatbox);
                textField.value = ''; // Clear input field after sending message
            });
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach((item, index) => {
            const className = item.name === "Sam" ? 'messages__item--visitor' : 'messages__item--operator';
            html += `<div class="messages__item ${className}">${item.message}</div>`;
        });

        const chatMessageContainer = chatbox.querySelector('.chatbox__messages');
        chatMessageContainer.innerHTML = html;
    }

    clearChat() {
        this.messages = []; // Clear chat history
        this.updateChatText(this.args.chatBox); // Update chatbox to clear messages
    }
}

const chatbox = new Chatbox();
chatbox.display();
$(document).ready(function() {
    
    $('.pour') //Pour Me Another Drink, Bartender!
      .delay(0)
      .animate({
        height: '150px'
        }, 1500)
      .delay(15600);
  
      $('.pourTube') //Pour Me Another Drink, Bartender!
        .delay(0)
        .animate({
          height: '150px'
          }, 0)
        .delay(15600);
  
    $('#liquid') // I Said Fill 'Er Up!
      .delay(1300)
      .animate({
        height: '170px'
      }, 15000);
  
    $('.beer-foam') // Keep that Foam Rollin' Toward the Top! Yahooo!
      .delay(3400)
      .animate({
        bottom: '200px'
        }, 2500);
    });
    // Add JavaScript to toggle the visibility of the user table when clicking the "Donors" button
document.addEventListener('DOMContentLoaded', function() {
    const donorsBtn = document.getElementById('donors-btn');
    const donorsTable = document.getElementById('donors-table');

    donorsBtn.addEventListener('click', function() {
        if (donorsTable.style.display === 'none') {
            donorsTable.style.display = 'table';
        } else {
            donorsTable.style.display = 'none';
        }
    });
});
