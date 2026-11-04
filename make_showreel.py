import subprocess, os
E = r"C:\Users\Александр\Projects\survival-studio\episodes"
clips = [("tsunami-beach",20),("forest-fire-tent",30),("tornado-highway",15),
         ("acid-rain-mall",25),("elevator-blackout",30),("avalanche-resort",20)]
D = 4.0
os.makedirs("tmp", exist_ok=True)
parts = []
for i,(ep,ss) in enumerate(clips):
    out = f"tmp/p{i}.mp4"
    subprocess.run(["ffmpeg","-y","-v","error","-ss",str(ss),"-t",str(D),"-i",os.path.join(E,ep,"final.mp4"),
        "-vf","scale=720:1280,fps=30,fade=t=in:st=0:d=0.25,fade=t=out:st=3.75:d=0.25",
        "-af","afade=t=in:st=0:d=0.25,afade=t=out:st=3.75:d=0.25,aresample=44100",
        "-c:v","libx264","-crf","26","-preset","medium","-c:a","aac","-b:a","128k","-ac","2",out],check=True)
    parts.append(out)
# title card
font = "C\:/Windows/Fonts/arialbd.ttf"
dt = (f"drawtext=fontfile='{font}':text='МОНТАЖ ВИДЕО':fontcolor=white:fontsize=64:x=(w-tw)/2:y=h/2-90,"
      f"drawtext=fontfile='{font}':text='Reels · Shorts · TikTok':fontcolor=0xF5B642:fontsize=40:x=(w-tw)/2:y=h/2+10,"
      f"fade=t=in:st=0:d=0.3,fade=t=out:st=1.7:d=0.3")
subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=0x111111:s=720x1280:r=30:d=2",
    "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-t","2","-vf",dt,
    "-c:v","libx264","-crf","26","-c:a","aac","-b:a","128k","tmp/title.mp4"],check=True)
with open("tmp/list.txt","w",encoding="utf-8") as f:
    for p in ["tmp/title.mp4"]+parts: f.write(f"file '{os.path.basename(p)}'\n")
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i","tmp/list.txt","-c","copy","-movflags","+faststart","video/showreel.mp4"],check=True)
subprocess.run(["ffmpeg","-y","-v","error","-ss","8","-i","video/showreel.mp4","-frames:v","1","-q:v","4","video/showreel-poster.jpg"],check=True)
print("ok")
