const client = require('discord-rich-presence')('917341970790244362');
const exec = require('child_process').exec;

const setTrack = (track) => {
  client.updatePresence({
    state: "Listenening to '" + "'",
    startTimestamp: Date.now(),
    instance: true
  });
}

const disable = () => {
}

setInterval(() => {
  exec('tasklist', function (err, stdout, stderr) {
    //see if AmazonMusic.exe is running
    if (stdout.includes('Amazon Music.exe')) {
      console.log('AmazonMusic.exe is running');
      setTrack();
    }
    else {
      console.log('AmazonMusic.exe is not running');
      disable();
    }
  });
}, 5000);

//https://github.com/NodeRT/NodeRT
//https://www.npmjs.com/package/@nodert-win10-rs4/windows.media.playback
//https://docs.microsoft.com/en-us/uwp/api/Windows.Media.Playback?redirectedfrom=MSDN&view=winrt-22000
//npm install @nodert-win10-rs4/windows.media.playback