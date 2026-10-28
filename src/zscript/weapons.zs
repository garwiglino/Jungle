class Cartouches : Ammo
{
 Default { Inventory.Amount 30; Inventory.MaxAmount 240; Inventory.PickupMessage "Munitions"; }
 States { Spawn: AMMO A -1; Stop; }
}
class ImpactCrique : BulletPuff
{
 Default { RenderStyle "Translucent"; Alpha 0.7; +NOGRAVITY; +NOBLOCKMAP; }
 States { Spawn: IMPA AB 3; Stop; }
}
class Fusil : Weapon
{
 int loaded;
 int capacity;
 override void PostBeginPlay() { Super.PostBeginPlay(); loaded=30; capacity=30; }
 Default
 {
  Weapon.SelectionOrder 100;
  Weapon.AmmoType1 "Cartouches";
  Weapon.AmmoUse1 0;
  Weapon.AmmoGive1 0;
  Weapon.SlotNumber 2;
  +WEAPON.AMMO_OPTIONAL;
  Inventory.PickupMessage "Fusil 5.56";
  Scale 0.5;
 }
 action void ReloadMagazine()
 {
  let w=Fusil(invoker);
  let reserve=FindInventory("Cartouches");
  if (!reserve) return;
  int n=min(w.capacity-w.loaded,reserve.Amount);
  w.loaded+=n; reserve.Amount-=n;
 }
 action void FireRound()
 {
  let w=Fusil(invoker);
  if (w.loaded<=0) { A_StartSound("crique/reload",CHAN_WEAPON,0,0.25); return; }
  w.loaded--;
  A_StartSound("crique/rifle",CHAN_WEAPON);
  A_FireBullets(1.6,1.2,1,14,"ImpactCrique",FBF_NORANDOM|FBF_NOFLASH);
  A_SetPitch(pitch-0.8);
  let p=Soldat(self); if(p) p.MakeNoise(70);
 }
 States
 {
 Spawn: FREN A -1; Stop;
 Select: FREN A 1 A_Raise; Loop;
 Deselect: FREN A 1 A_Lower; Loop;
 Ready: FREN A 1 A_WeaponReady(WRF_ALLOWRELOAD); Loop;
 Fire: FREN B 2 FireRound; FREN C 3; FREN A 0 A_ReFire; Goto Ready;
 Reload: FREN D 5 A_StartSound("crique/reload",CHAN_WEAPON);
  FREN E 10; FREN F 10; FREN G 6 ReloadMagazine; FREN H 4; Goto Ready;
 }
}
class PAM : Fusil
{
 override void PostBeginPlay() { Super.PostBeginPlay(); capacity=12; loaded=12; }
 Default { Weapon.SlotNumber 1; Weapon.SelectionOrder 200; Inventory.PickupMessage "Pistolet 9 mm"; }
 action void FirePistol()
 {
  let w=Fusil(invoker); if(w.loaded<=0) return;
  w.loaded--; A_StartSound("crique/pistol",CHAN_WEAPON);
  A_FireBullets(1,1,1,19,"ImpactCrique",FBF_NORANDOM|FBF_NOFLASH);
  A_SetPitch(pitch-1.2);
  let p=Soldat(self); if(p) p.MakeNoise(45);
 }
 States
 {
 Spawn: PAM9 A -1; Stop;
 Select: PAM9 A 1 A_Raise; Loop;
 Deselect: PAM9 A 1 A_Lower; Loop;
 Ready: PAM9 A 1 A_WeaponReady(WRF_ALLOWRELOAD); Loop;
 Fire: PAM9 B 2 FirePistol; PAM9 C 5; PAM9 H 3; Goto Ready;
 Reload: PAM9 D 4 A_StartSound("crique/reload",CHAN_WEAPON);
  PAM9 E 7; PAM9 F 8; PAM9 G 5 ReloadMagazine; PAM9 H 4; Goto Ready;
 }
}
