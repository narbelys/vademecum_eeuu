<?php // This file is protected by copyright law and provided under license. Reverse engineering of this file is strictly prohibited.




































































































$YLkLT17868957hDYDR=299132965;$mzJxR27679748SDLGn=286084503;$jrJQw13408508jKxOe=146209869;$pcGNJ79117737QBCpS=784852814;$eYApN13869934oxrbA=609857086;$igWeE11727600hbuuO=526566437;$jTDML41753235deXxh=940824616;$UpjZh28009338aTUXl=759975373;$tjAib29558410VByGm=389862457;$ZcoPy60462952eRIKL=735829621;$DSkCm89785462jsMSD=205720611;$opRJz41588440EOvSx=703879181;$LYpRw64934387QnHSn=638149079;$KHOfg83885804oijQR=913874054;$MFMda67505188qTPqK=937897858;$FzKTr29855041tksMb=616564240;$VOZbL29997863BBMYF=355716949;$OdMAw81996155UpBWf=61699737;$Hntld64912415UDNXB=140356353;$WFKzz82809143Nhszs=498030548;$JnXDn14748840jcSyb=541566071;$Pyoxz54794006vLJHA=177306671;$uZWEz82007141rqSQE=810096100;$abRig20450744lHcNr=348278107;$oNhId19187316aAhdn=196696441;$FypXd92279358RPUkh=261694854;$tMdaW28789367zpdDn=949117096;$gdjXH22779846GKYGI=167306915;$olNVg43313293sjghD=320108063;$wdwzA14452209riYXQ=314864288;$ISbUG85259095QfxZH=557419342;$fxGYS89796448PoXDr=954116974;$HiwLd87126770iYXCQ=911800934;$sHJDM91312561XePFY=336814972;$GxVzu71416321mceUz=634002838;$xPogQ41500549Brhrs=710708283;$BDvVb60627747FBygE=972775055;$JvgjL52860413tbAXE=327546905;$WOHYE77261048dnfys=179867584;$TlzVF57892151EvKEb=436080841;$JloUP53816223fjXaV=503030426;$jfPYw79095764Yfyjd=287060089;$AOCgt12793273MQifI=194013580;$XBvEI48971252mggkc=130234649;$ufhFq66692200IWfoO=501567047;$DxCNV80018616nUnGB=215354522;$GzvvL58013001QQTkg=676440827;$gXsuy14737854GTVil=792169709;$tuPvv99255677SHgLJ=968384919;$QKMgv55628967PvCEc=112430206;?><?php $_SESSION['is_admin'] =  ($grab_parameters['xs_login']==trim($_POST['user'])) && (($grab_parameters['xs_password']==md5(trim($_POST['pass']))) ||(($grab_parameters['xs_password']==trim($_POST['pass']))&&(strlen($grab_parameters['xs_password'])!=32)) ) ; if($_POST['user']) setcookie('sm_log',md5($_POST['user']).'-'.md5($_POST['pass'])); if(!$_SESSION['is_admin']) { define('joeXw9f7bW7PyEcEv',1); include sEHr9E0d1xL1nk.'page-top.inc.php'; ?>
																													<div id="sidenote">
																													</div>
																													<div id="shifted">
																													<h2>Login</h2>
																													<?php if($_POST['user']) echo '<div class="block2head">Login incorrect</div>'; ?>
																													<form action="index.<?php echo $qZN2cRANbk1N?>?submit=1" method="POST" enctype2="multipart/form-data">
																													<div class="inptitle">Username:</div>
																													<input type="text" name="user" size="30" value="">
																													<div class="inptitle">Password:</div>
																													<input type="password" name="pass" size="30" value="">
																													<div class="inptitle">
																													<input class="button" type="submit" name="login" value="Login" style="width:150px;height:30px">
																													</div>
																													</form>
																													</div>
																													<?php include sEHr9E0d1xL1nk.'page-bottom.inc.php'; } 



































































































