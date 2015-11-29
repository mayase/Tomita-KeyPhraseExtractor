#encoding "utf-8" 
#GRAMMAR_ROOT S     

S -> Adj<gnc-agr[1]>+ Noun<gnc-agr[1],rt>;
Name -> Word<h-reg1, gram="имя">;
Surname -> Word<h-reg1, gram="фам">;
S -> Name<gnc-agr[1],rt> Surname<gnc-agr[1]>;
S -> Noun;
S -> "деньги";
S -> Noun Noun<gram="gen">; 
S -> Noun Prep Noun;
S -> Noun Noun Prep Noun;
S -> Noun Prep Noun Noun;