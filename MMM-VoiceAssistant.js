Module.register('MMM-VoiceAssistant',
{
    defaults:
    {
        header: "Voice assistant",
        updateDelay: 500,
        maxWidth: "100%",
        scale: 1
    },
    
    start: function()
    {
        var self = this;
        Log.info('Module: '+ this.name+" launched.");
        this.sendSocketNotification('INITIALIZE');
        
        setInterval(function() {
            self.updateDom(); // no speed defined, so it updates instantly.
        }, 1000); //perform every 1000 milliseconds.
        this.assistantActive = false;
        this.response = null;
    },

    getDom: function() {
        const element = document.createElement("div");
        element.style = 'display: flex; justify-content: space-between; align-items: center; flex-direction: row;';
        const image = document.createElement("img");
        const text = document.createElement("div");

        if (!this.assistantActive){
            image.style = `transform:scale(${this.config.scale})`;
            image.src = this.file("resources/images/assistant_inactive.png");   
            element.appendChild(image);
        }
        else{
            image.style = `transform:scale(${this.config.scale})`;
            image.src = this.file("resources/images/assistant_active.png");   
            
            text.innerHTML = this.response;
            // "Hello world!";
            text.style = 'font-family: Roboto; font-weight: normal; font-size: 25px; padding-left: 15px; padding-right: 15px;'
            text.style.border = "thin solid #ffffff";
            text.style.borderRadius = "2em";
            text.style.textAlign = "center"
            element.appendChild(image);
            element.appendChild(text);
        }

        
        return element;

    },


    socketNotificationReceived: function(notification, payload) {
        console.log("Notification: ")
        console.log(notification)
        console.log(payload)


        if(notification==='ASSISTANT_ACTIVATED'){

            this.assistantActive = true;
            this.response = '...'
            this.updateDom();
        }
        else if(notification==='COMMAND_SENT'){
            this.assistantActive = true;
            this.response = payload;
            this.updateDom();
        }
        else if(notification==='ASSISTANT_DEACTIVATED'){
            this.assistantActive = false;
            this.updateDom();
        }
    }

})