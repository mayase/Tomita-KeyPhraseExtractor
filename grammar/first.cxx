#encoding "utf-8" 
#GRAMMAR_ROOT S     


S -> Adj<gnc-agr[1]> "год"<gnc-agr[1],rt>;
S -> Adj<gnc-agr[1]> "месяц"<gnc-agr[1],rt>;
S -> Noun<gnc-agr[1]> "рубль"<gnc-agr[1],rt>;
S -> "в" | "с" | "а" | "я" | "и" | "ли" | "о" | "до" | "год";
