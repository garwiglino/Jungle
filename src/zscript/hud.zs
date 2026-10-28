class CriqueHUD : EventHandler
{
 override void RenderOverlay(RenderEvent e)
 {
  let p=Soldat(players[consoleplayer].mo); if(!p) return;
  String objective=p.recovered?"REJOINDRE LA BALISE / CRIQUE SUD":"RECUPERER LA VALISE / CAMP AU NORD";
  Screen.DrawText(SmallFont,Font.CR_WHITE,14,14,"CRIQUE / OPERATION LISIERE",DTA_VirtualWidth,640,DTA_VirtualHeight,360);
  Screen.DrawText(SmallFont,Font.CR_GREEN,14,29,objective,DTA_VirtualWidth,640,DTA_VirtualHeight,360);
  Screen.DrawText(SmallFont,Font.CR_WHITE,14,326,String.Format("SANTE %d",p.health),DTA_VirtualWidth,640,DTA_VirtualHeight,360);
  let w=Fusil(p.player.ReadyWeapon); let a=p.FindInventory("Cartouches");
  if(w) Screen.DrawText(SmallFont,Font.CR_WHITE,390,326,String.Format("%s  %d / %d",w.GetClassName() == 'MAT49Preview'?"MAT 49":w is "PAM"?"9 MM":"5.56",w.loaded,a?a.Amount:0),DTA_VirtualWidth,640,DTA_VirtualHeight,360);
  Screen.DrawText(SmallFont,Font.CR_GRAY,14,343,"E INTERAGIR  |  R RECHARGER  |  1/2 ARMES  |  F6 SAUVER",DTA_VirtualWidth,640,DTA_VirtualHeight,360);
  // Pixel-centered reticle, independent of sprite pose and view aspect ratio.
  double cx=Screen.GetWidth()*0.5, cy=Screen.GetHeight()*0.5;
  double rs=max(1.,Screen.GetHeight()/360.);
  Screen.DrawLine(cx-7*rs,cy,cx-3*rs,cy,"#9DE8CF");
  Screen.DrawLine(cx+3*rs,cy,cx+7*rs,cy,"#9DE8CF");
  Screen.DrawLine(cx,cy-7*rs,cx,cy-3*rs,"#9DE8CF");
  Screen.DrawLine(cx,cy+3*rs,cx,cy+7*rs,"#9DE8CF");
  if(p.health<=0) Screen.DrawText(SmallFont,Font.CR_RED,180,155,"MISSION INTERROMPUE / F9 CHARGER",DTA_VirtualWidth,640,DTA_VirtualHeight,360);
  if(p.complete)
  {
   Screen.Dim("#10251E",0.85,0,0,Screen.GetWidth(),Screen.GetHeight());
   Screen.DrawText(BigFont,Font.CR_GREEN,140,120,"EXTRACTION REUSSIE",DTA_VirtualWidth,640,DTA_VirtualHeight,360);
   Screen.DrawText(SmallFont,Font.CR_WHITE,155,175,"VALISE SECURISEE / MISSION TERMINEE",DTA_VirtualWidth,640,DTA_VirtualHeight,360);
   Screen.DrawText(SmallFont,Font.CR_WHITE,155,196,String.Format("DUREE %d:%02d / ESC MENU",p.finishTime/2100,(p.finishTime/35)%60),DTA_VirtualWidth,640,DTA_VirtualHeight,360);
  }
 }
}

class CriqueBar : BaseStatusBar {}
