const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const V=process.argv[2]==='vertical';const FPS=30,DUR=27,T0=V?17.5:0,OUT=V?'NH_ONE_Reel_End_9x16.mp4':'NH_ONE_Intro.mp4';const b=await chromium.launch();const p=await b.newPage({viewport:V?{width:1080,height:1920}:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/intro.html#render'+(V?'-vertical':''));await p.evaluate(()=>window.ready);
const ff=spawn('ffmpeg',['-y','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-',...(V?['-ss',String(T0)]:[]),'-i','music.wav',...(V?['-af','afade=t=in:d=0.15']:[]),'-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',OUT],{stdio:['pipe','ignore','inherit']});
for(let f=0;f<Math.round(FPS*(DUR-T0));f++){const data=await p.evaluate(t=>{render(t);return document.getElementById('c').toDataURL('image/png')},T0+f/FPS);
  const buf=Buffer.from(data.split(',')[1],'base64');if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%90==0)console.log('frame',f);}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();})();
