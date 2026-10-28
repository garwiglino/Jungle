// AI is deliberately bounded: no squad tactics, no navigation mesh.
class Milicien : Actor
{
 int mode; // 0 patrol, 1 investigate, 2 alert
 int memory;
 int cooldown;
 int patrolTick;
 Vector3 home;
 Vector3 investigate;
 Default
 {
  Health 75; Radius 18; Height 56; Speed 6;
  +SOLID; +SHOOTABLE; +COUNTKILL; +NOBLOOD;
  PainChance 0;
 }
 override void PostBeginPlay() { Super.PostBeginPlay(); home=pos; }
 override void Tick()
 {
  Super.Tick();
  if(health<=0) return;
  if(cooldown>0) cooldown--;
  if(level.maptime%5 != 0) return;
  let p=Soldat(players[0].mo);
  if(!p || p.health<=0 || p.complete) return;
  double dist=Distance2D(p);
  double diff=abs(DeltaAngle(angle,AngleTo(p)));
  double sightRange=(p.player.cmd.buttons & BT_CROUCH)?420:850;
  bool visible=dist<sightRange && (diff<55 || dist<110) && CheckSight(p);
  if(visible) { mode=2; memory=210; target=p; investigate=p.pos; }
  else if(mode==2)
  {
   memory-=5;
   if(memory<=0) { mode=1; target=null; }
  }
  if(!visible && mode!=2 && level.maptime<p.noiseUntil && dist<1100)
  {
   mode=1; investigate=p.lastNoise;
  }
  Vector3 dest=home;
  if(mode==0)
  {
   patrolTick+=5;
   dest=home+ (cos(patrolTick*.5)*120,sin(patrolTick*.5)*120,0);
  }
  else dest=investigate;
  if(mode==2 && visible && dist<620)
  {
   angle=AngleTo(p);
   if(cooldown==0)
   {
    A_StartSound("crique/pistol",CHAN_WEAPON,0,0.6);
    A_CustomBulletAttack(7,5,1,5,"ImpactCrique");
    cooldown=35;
   }
  }
  else
  {
   Vector2 delta=dest.xy-pos.xy;
   if(delta.Length()>40)
   {
    angle=VectorAngle(delta.x,delta.y);
    Vector2 step=(cos(angle),sin(angle))*(mode==2?10:5);
    if(!TryMove(pos.xy+step,0))
    {
     angle+=90; TryMove(pos.xy+(cos(angle),sin(angle))*6,0);
    }
   }
   else if(mode==1) { mode=0; }
  }
 }
 States
 {
 Spawn: MLTC AB 8; Loop;
 Death: MLTC D 1 A_NoBlocking; MLTC D -1; Stop;
 }
}
class Raptor : Milicien
{
 Default { Health 110; Radius 23; Height 48; }
 override void Tick()
 {
  // Reuse detection/patrol, but suppress the parent's ranged attack.
  if(cooldown<15) cooldown=15;
  Super.Tick();
  if(health<=0 || mode!=2 || !target || level.maptime%5!=0) return;
  angle=AngleTo(target);
  if(Distance2D(target)<65 && CheckSight(target))
  {
   if(memory>0 && level.maptime%35==0)
   { target.DamageMobj(self,self,12,'Melee'); A_StartSound("crique/call",CHAN_VOICE); }
  }
  else TryMove(pos.xy+(cos(angle),sin(angle))*14,0);
 }
 States
 {
 Spawn: RAPT ABC 6; Loop;
 Death: RAPT D 1 A_NoBlocking; RAPT D -1; Stop;
 }
}
class GrandArbre : Actor
{
 Default { Radius 22; Height 210; +SOLID; Scale 1.3; }
 States { Spawn: TREE A -1; Stop; }
}
class Fougere : Actor
{
 Default { Radius 8; Height 36; Scale 0.7; +NOBLOCKMAP; }
 States { Spawn: FERN A -1; Stop; }
}
class DataCase : Actor
{
 Default { Radius 24; Height 24; Scale 0.65; }
 override void Tick()
 {
  Super.Tick();
  let p=Soldat(players[0].mo);
  if(p && !p.recovered && p.health>0 && Distance2D(p)<90 && (p.player.cmd.buttons & BT_USE) && CheckSight(p))
  {
   p.recovered=true; p.A_StartSound("crique/pickup",CHAN_ITEM); Destroy();
  }
 }
 States { Spawn: CASE A -1; Stop; }
}
class Extraction : Actor
{
 Default { Radius 32; Height 48; Scale 1.0; }
 override void PostBeginPlay() { Super.PostBeginPlay(); A_StartSound("crique/ambient",CHAN_BODY,CHANF_LOOPING,0.5,ATTN_NONE); }
 override void Tick()
 {
  Super.Tick(); let p=Soldat(players[0].mo);
  if(p && p.health>0 && p.recovered && !p.complete && Distance2D(p)<130 && (p.player.cmd.buttons & BT_USE))
  { p.complete=true; p.finishTime=level.maptime; p.player.cheats|=CF_FROZEN; A_StartSound("crique/pickup",CHAN_ITEM); }
 }
 States { Spawn: BEAC A -1; Stop; }
}
class Trousse : Health
{
 Default { Inventory.Amount 35; Inventory.MaxAmount 100; Inventory.PickupMessage "Trousse : +35 sante"; Inventory.PickupSound "crique/pickup"; Scale 0.5; }
 States { Spawn: MEDI A -1; Stop; }
}
class Reserve : Cartouches
{
 Default { Inventory.Amount 45; Inventory.PickupMessage "Reserve : 45 cartouches"; Scale 0.5; }
}
class Caisse : Actor
{
 Default { Radius 34; Height 44; +SOLID; }
 States { Spawn: CASE A -1; Stop; }
}
class Pirogue : Actor
{
 Default { Radius 78; Height 30; +SOLID; }
 States { Spawn: CASE A -1; Stop; }
}
