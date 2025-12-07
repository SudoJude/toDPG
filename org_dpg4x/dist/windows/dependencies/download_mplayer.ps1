# Powershell script to download mplayer from SourceForge. Built in NSIS downloaders couldn't handle that page

$src=$args[0]
if ($src -eq $null) {
	$src = "http://sourceforge.net/projects/mplayer-win32/files/MPlayer%20and%20MEncoder/r38188%2Bg6e1903938b/MPlayer-x86_64-r38188%2Bg6e1903938b.7z/download"
}
$dest=$args[1]
if ($dest -eq $null) {
	$dest = "c:\tmp\MPlayer-x86_64-r38188+Bg6e1903938b.7z"
}

$client = new-object System.Net.WebClient
$client.DownloadFile($src, $dest)