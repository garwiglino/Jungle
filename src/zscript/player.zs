class Soldat : PlayerPawn
{
 int noiseUntil;
 Vector3 lastNoise;
 bool recovered;
 bool complete;
 int finishTime;
 Default
 {
  Speed 0.85; Health 100; Radius 16; Height 56;
  Player.DisplayName "Soldat francais";
  Player.ViewHeight 41;
  Player.StartItem "Fusil";
  Player.StartItem "PAM";
  Player.StartItem "Cartouches", 150;
  Player.WeaponSlot 1, "PAM";
  Player.WeaponSlot 2, "Fusil";
 }
 void MakeNoise(int duration)
 {
  noiseUntil = level.maptime + duration;
  lastNoise = pos;
 }
 override void Tick()
 {
  Super.Tick();
  if (health <= 0) return;
  if ((player.cmd.buttons & BT_SPEED) && Vel.LengthSquared() > 5 && !(player.cmd.buttons & BT_CROUCH)) MakeNoise(5);
 }
 States
 {
 Spawn: MLTC A -1; Loop;
 See: MLTC AB 4; Loop;
 Pain: MLTC C 4; Goto Spawn;
 Death: MLTC D -1; Stop;
 }
}
