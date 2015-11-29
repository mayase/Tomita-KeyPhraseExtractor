#encoding "utf-8" 
#GRAMMAR_ROOT S     

Name -> Word<h-reg1, gram="имя">;
Surname -> Word<h-reg1>;
S -> Name<gnc-agr[1],rt> (Surname<gnc-agr[1]>);