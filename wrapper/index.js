var express = require('express'),
    app = express(),
    PORT = 8080;


var bodyParser = require('body-parser');
app.use(bodyParser.json());


var redis = require('redis'),
    client = redis.createClient();


app.post("/*", (req, res) => {
	var alertname = req.body.commonLabels.alertname;
	var miner = req.body.commonLabels.instance.split(":",1)[0];
	if ( alertname == "InstanceDown" ) {
		var spawn = require("child_process").spawn;
		var pythonProcess = spawn('python',["interface.py", miner, "reboot"]);
		//pythonProcess.stdout.on('data', function (data) {
		//});
		console.log(miner+" REBOOT!");
		res.send("OK")

	} else if ( alertname == "LoseGPU" ) {
		var devid = req.body.commonLabels.devid;
		var spawn = require("child_process").spawn;
		var pythonProcess = spawn('python',["interface.py", miner, "decreaseFreq", devid]);
		pythonProcess.stdout.on('data', function (data) {
		});
		console.log(miner+" "+devid+" DECREASE FREQ!");
		res.send("OK")
	} else {
		console.log(req.body)
		console.log("Trivial message as above!")
		res.send("OK")
	}
});

app.get("/miner/*", (req, res) => {
        miner = 'miner'+req.query.id;
        client.hgetall(miner, function(err, obj) {
           res.send(obj);
        });
});

app.get("/mac/*", (req, res) => {
        mac = req.query.id;
        client.get(mac, function(err, obj) {
           res.send(obj);
        });
});

app.get("/ip/*", (req, res) => {
        ip = req.query.id;
        client.get(ip, function(err, obj) {
           res.send(obj);
        });
});

//app.post('/reboot', (req, res) => {
//	var evalMatches = req.body.evalMatches;
//	var state = req.body.state;
//
//	if ( state == "alerting" ) {
//		//console.log(evalMatches);
//		for ( obj of evalMatches ) {
//			console.log(obj)
//			miner = obj.metric.split("instance=\"")[1].split(":",1)[0]
//			var spawn = require("child_process").spawn;
//			var pythonProcess = spawn('python',["interface.py", miner, "reboot"]);
//			pythonProcess.stdout.on('data', function (data) {
//				// Do something with the data returned from python script
//			});
//			console.log(miner+" REBOOT!");
//		};
//	}
//
//	res.send("OK\n");
//});
//
//app.post('/decreaseFreq', (req, res) => {
//	var evalMatches = req.body.evalMatches;
//	var state = req.body.state;
//
//	if ( state == "alerting" ) {
//		//console.log(evalMatches);
//		for ( obj of evalMatches ) {
//			miner = obj.metric.split("instance=\"")[1].split(":",1)[0]
//			devid = obj.metric.split("devid=\"")[1].split(":",1)[0]
//			var spawn = require("child_process").spawn;
//			var pythonProcess = spawn('python',["interface.py", miner, "decreaseFreq", devid]);
//			pythonProcess.stdout.on('data', function (data) {
//				// Do something with the data returned from python script
//			});
//			console.log(miner+" "+devid+" DECREASE FREQ!");
//		};
//	}
//
//	res.send("OK\n");
//});
//
//app.post('/increaseFreq', (req, res) => {
//	var evalMatches = req.body.evalMatches;
//	var state = req.body.state;
//
//	if ( state == "alerting" ) {
//		//console.log(evalMatches);
//		for ( obj of evalMatches ) {
//			miner = obj.metric.split("instance=\"")[1].split(":",1)[0]
//			devid = obj.metric.split("devid=\"")[1].split(":",1)[0]
//			var spawn = require("child_process").spawn;
//			var pythonProcess = spawn('python',["interface.py", miner, "increaseFreq", devid]);
//			pythonProcess.stdout.on('data', function (data) {
//				// Do something with the data returned from python script
//			});
//			console.log(miner+" "+devid+" INCREASE FREQ!");
//		};
//	}
//
//	res.send("OK\n");
//});

app.listen(PORT);
console.log('Running on localhost:'+PORT);
