const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const FPS=30,DUR=27;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/intro.html#render');await p.evaluate(()=>window.ready);
const ff=spawn('ffmpeg',['-y','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-','-i','music.wav','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','NH_ONE_Intro.mp4'],{stdio:['pipe','ignore','inherit']});
for(let f=0;f<FPS*DUR;f++){const data=await p.evaluate(t=>{render(t);return document.getElementById('c').toDataURL('image/png')},f/FPS);
  const buf=Buffer.from(data.split(',')[1],'base64');if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%90==0)console.log('frame',f);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();})();
