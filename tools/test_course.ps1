param([Parameter(Mandatory)][string]$Course)
# Headless-Edge walkthrough of one built course (ai, design, robot). Prints one result line; "bad=[]" and no ERR/EX means pass.
$root  = Split-Path $PSScriptRoot -Parent
$edge  = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
$tmp   = Join-Path $env:TEMP "course-test-$Course"
New-Item -ItemType Directory -Force $tmp | Out-Null
$js = @'
<script>
var log=[];window.onerror=function(m,s,l){log.push('ERR '+m+' @'+l)};
setTimeout(function(){try{
 var bad=[];
 LESSONS.forEach(function(l){
   if(l.steps.length!==3) bad.push(l.id+' steps');
   var qs=testQs(l); if(qs.length!==10) bad.push(l.id+' qs='+qs.length);
   qs.forEach(function(q,i){ if(!(q.a>=0&&q.a<q.o.length)) bad.push(l.id+' q'+i); });
   if(!MEDIA[l.id]) bad.push(l.id+' nomedia');
 });
 var media=0, vids=0;
 LESSONS.forEach(function(l,li){
   go({name:'lesson',id:l.id});
   l.steps.forEach(function(st,k){ document.querySelector('[data-act=step][data-k="'+k+'"][data-i="'+st.q.a+'"]').click(); });
   if(document.getElementById('sec-media')) media++; vids+=document.querySelectorAll('[data-act=play]').length;
   var w=document.querySelector('[data-act=mx],[data-act=pc],[data-act=sv]'); if(w) w.click();
   l.cards.forEach(function(_,i){ document.querySelector('[data-act=card][data-side=t][data-i="'+i+'"]').click(); document.querySelector('[data-act=card][data-side=d][data-i="'+i+'"]').click(); });
   testQs(l).forEach(function(q,qi){ var pick = (li===0 && qi===3) ? (q.a+1)%q.o.length : q.a; document.querySelector('[data-act=tpick][data-q="'+qi+'"][data-i="'+pick+'"]').click(); });
   document.querySelector('[data-act=submit]').click();
   if(!L(l.id).passed) bad.push('notpassed '+l.id);
 });
 log.push('lessons='+LESSONS.length+' bad=['+bad.join(',')+'] mediaBlocks='+media+' videos='+vids);
 log.push('xp='+S.xp+' badges='+S.badges.length+' wrong='+wrongCount()+' streak='+S.streak.n);
 go({name:'review'}); log.push('reviewCards='+document.querySelectorAll('.rv .card').length);
 document.querySelector('[data-act=unwrong]').click(); log.push('afterUnwrong='+wrongCount());
 go({name:'home'}); log.push('stairsOn='+document.querySelectorAll('.stair.on').length+' thumbs='+document.querySelectorAll('.les .th img').length+' menu='+document.querySelectorAll('.menu a').length);
 document.querySelector('[data-act=fs]').click(); log.push('fs='+getComputedStyle(document.documentElement).getPropertyValue('--fs').trim());
 go({name:'glossary'}); log.push('gl='+document.querySelectorAll('.gl-row').length+' title='+document.title);
}catch(e){log.push('EX '+e.message)} document.body.setAttribute('data-log',log.join(' | '));},500);
</script>
'@
$html = [IO.File]::ReadAllText((Join-Path $root "$Course\index.html"), [Text.Encoding]::UTF8)
$t = Join-Path $tmp "page.html"
[IO.File]::WriteAllText($t, $html.Replace("</body>", $js + "</body>"), (New-Object Text.UTF8Encoding $false))
$o = Join-Path $tmp "dom.txt"
Start-Process -FilePath $edge -ArgumentList "--headless","--disable-gpu","--no-first-run","--user-data-dir=`"$tmp\ud`"","--virtual-time-budget=8000","--dump-dom","`"file:///$($t -replace '\\','/')`"" -RedirectStandardOutput $o -RedirectStandardError (Join-Path $tmp "err.txt") -Wait -NoNewWindow
"$Course : " + [regex]::Match([IO.File]::ReadAllText($o, [Text.Encoding]::UTF8), 'data-log="[^"]*"').Value
