let { PythonShell } = require("python-shell");

const NodeHelper = require('node_helper');


module.exports = NodeHelper.create({

    start_script: function() {

        //const pyshell = new PythonShell('wakeup.py', null);

        PythonShell.run('modules/MMM-VoiceAssistant/assistant.py', null, function (err, results) {
          });

    },
    
    socketNotificationReceived: function(notification) {

        if(notification === 'INITIALIZE')
        {
            this.start_script();

        }
    },

    notificationReceived: function(){
        
    }
    
});

   