import subprocess,os,time,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
env=dict(os.environ,DISPLAY=':99',LD_LIBRARY_PATH=str(ROOT/'vendor/local/usr/lib/x86_64-linux-gnu'))
xdo=shutil.which('xdotool') or str(ROOT/'vendor/local/usr/bin/xdotool')
def key(*args):subprocess.run([xdo,*args],env=env,check=True)
def command(s):
 key('key','grave'); time.sleep(.3); key('type','--delay','45',s); key('key','Return'); time.sleep(3 if s.startswith(('map ','load ')) else .3); key('key','grave'); time.sleep(.5)
def shot(name):subprocess.run(['ffmpeg','-y','-f','x11grab','-video_size','1280x720','-i',':99','-frames:v','1',str(ROOT/'reports'/name),'-loglevel','error'],check=True)
if __name__=='__main__':
 command('summon CriqueProbe')
 key('mousedown','1'); time.sleep(.7); key('mouseup','1'); command('summon CriqueProbe'); shot('rifle-fired.png')
 key('keydown','r'); time.sleep(.2); key('keyup','r'); time.sleep(1.5); command('summon CriqueProbe'); shot('rifle-reloaded.png')
 key('key','1');time.sleep(1);key('mousedown','1');time.sleep(.2);key('mouseup','1');time.sleep(.5);command('summon CriqueProbe');shot('pistol-fired.png')
 command('warp 2176 384');key('keydown','e');time.sleep(.3);key('keyup','e');command('summon CriqueProbe')
 command('god');command('warp 2150 5700');key('keydown','e');time.sleep(.4);key('keyup','e');command('summon CriqueProbe');shot('objective.png')
 command('save checkpoint');time.sleep(1);command('warp 2176 384');command('load checkpoint');time.sleep(2);command('summon CriqueProbe');shot('restored.png')
 command('warp 2176 384');key('keydown','e');time.sleep(.4);key('keyup','e');command('summon CriqueProbe');shot('extraction.png')
 command('map MAP01');time.sleep(1);command('summon CriqueRouteTest');time.sleep(1)
 command('quit')
