const { PythonShell } = require("python-shell");

const NodeHelper = require('node_helper');

// const PythonShell  = require('python-shell');


const prepareDataForModule = (data) => {
    console.log('Data to parse: '+ data)
    const answer = JSON.parse(data);
    // const splittedData = data.replace('{', '').replace('}','').split(':');
    const objToTransfer = {'status':answer.status, 'assistant_response':answer.assistant_response};
    console.log(objToTransfer);
    return objToTransfer;
}

const prepareDataForChangingState = (data) => {
    console.log('Data to parse: '+ data)
    const answer = JSON.parse(data);
    const objToTransfer = {'status':answer.status};
    return objToTransfer;
}

module.exports = NodeHelper.create({

    start_script: function() {
        const self = this;
        console.log('assistant STARTED');

        const pyshell = new PythonShell('modules/MMM-VoiceAssistant/assistant.py', {mode:'text'});

        pyshell.on('message', function(data){

            if(data.includes('COMMAND_SENT')){
                const preparedData = prepareDataForModule(data);
                self.sendSocketNotification(preparedData.status, preparedData.assistant_response);
            }
            else if (data.includes('ASSISTANT_ACTIVATED')||data.includes('ASSISTANT_DEACTIVATED')){
                const preparedHeader = prepareDataForChangingState(data);
                self.sendSocketNotification(preparedHeader.status);
            }

            console.log(data);

        });

        pyshell.end(function (err){
            if (err) throw err;
            console.log('Assistant fatal')
            console.log(err)

        })
        
       

        // PythonShell.run('modules/MMM-VoiceAssistant/assistant.py', null, function (err, results) {
        //     if (err) throw err;
        //   // result is an array consisting of messages collected during execution of script.
        //   console.log('result: ', results.toString());
        //   });

    },
    
    socketNotificationReceived: function(notification) {

        if(notification === 'INITIALIZE')
        {
            this.start_script();

        }
    },

    notificationReceived: function(){
        
    },
    
    //this.sendSocketNotification('ASSISTANT_ACTIVATED')
    
});

   