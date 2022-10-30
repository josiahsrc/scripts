var YoutubeMp3Downloader = require("youtube-mp3-downloader");

// Takes in a URL to a youtube video and returns a promise that resolves to the URL of the mp3 file. The mp3 file is
// saved to the local filesystem.
//
// Usage: `to-mp3.js <youtube-url>`
async function main() {
  var url = process.argv[2];
  var outDir = process.argv[3] || __dirname;
  if (!url) {
    console.error('Usage: to-mp3.js <youtube-url> [out-dir]');
    process.exit(1);
  }

  // parse out the id from the youtube url
  var id = url.split('v=')[1];
  if (!id) {
    console.error('Invalid youtube url');
    process.exit(1);
  }

  var YD = new YoutubeMp3Downloader({
    "ffmpegPath": "/opt/homebrew/bin/ffmpeg", 
    "outputPath": outDir,
    "youtubeVideoQuality": "highestaudio",
    "queueParallelism": 2,
    "progressTimeout": 2000, 
    "allowWebm": false
  });

  YD.download(id);

  YD.on("finished", function(err, data) {
    console.log(JSON.stringify(data));
  });

  YD.on("error", function(error) {
    console.log(error);
  });

  YD.on("progress", function(progress) {
    console.log(JSON.stringify(progress));
  });
}

main();
