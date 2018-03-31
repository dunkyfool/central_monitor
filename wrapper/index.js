var express = require('express'),
    app = express(),
    PORT = 8080;


var bodyParser = require('body-parser');
app.use(bodyParser.json());


app.post('/reboot', (req, res) => {
	var evalMatches = req.body.evalMatches;
	var state = req.body.state;

	if ( state == "alerting" ) {
		//console.log(evalMatches);
		for ( obj of evalMatches ) {
			console.log(obj)
			miner = obj.metric.split("instance=\"")[1].split(":",1)[0]
			var spawn = require("child_process").spawn;
			var pythonProcess = spawn('python',["interface.py", miner, "reboot"]);
			pythonProcess.stdout.on('data', function (data) {
				// Do something with the data returned from python script
			});
			console.log(miner+" REBOOT!");
		};
	}

	res.send("OK\n");
});

app.post('/decreaseFreq', (req, res) => {
	var evalMatches = req.body.evalMatches;
	var state = req.body.state;

	if ( state == "alerting" ) {
		//console.log(evalMatches);
		for ( obj of evalMatches ) {
			miner = obj.metric.split("instance=\"")[1].split(":",1)[0]
			var spawn = require("child_process").spawn;
			var pythonProcess = spawn('python',["interface.py", miner, "decreaseFreq"]);
			pythonProcess.stdout.on('data', function (data) {
				// Do something with the data returned from python script
			});
			console.log(miner+" DECREASE FREQ!");
		};
	}

	res.send("OK\n");
});

app.post('/increaseFreq', (req, res) => {
	var evalMatches = req.body.evalMatches;
	var state = req.body.state;

	if ( state == "alerting" ) {
		//console.log(evalMatches);
		for ( obj of evalMatches ) {
			miner = obj.metric.split("instance=\"")[1].split(":",1)[0]
			var spawn = require("child_process").spawn;
			var pythonProcess = spawn('python',["interface.py", miner, "increaseFreq"]);
			pythonProcess.stdout.on('data', function (data) {
				// Do something with the data returned from python script
			});
			console.log(miner+" INCREASE FREQ!");
		};
	}

	res.send("OK\n");
});

app.listen(PORT);
console.log('Running on localhost:'+PORT);
