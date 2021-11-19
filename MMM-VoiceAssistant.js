Module.register('MMM-VoiceAssistant',
{
    defaults:
    {
        header: "Voice assistant"
    },
    
    start: function()
    {
        var self = this;
        Log.info('Module: '+ this.name+" launched.");
        this.sendSocketNotification('INITIALIZE', this.config);
        
        setInterval(function() {
            self.updateDom(); // no speed defined, so it updates instantly.
        }, 1000); //perform every 1000 milliseconds.
    },

    getDom: function() {
        var wrapper = document.createElement("div");
        wrapper.innerHTML = "Hello world!";
        return wrapper;

    }

})