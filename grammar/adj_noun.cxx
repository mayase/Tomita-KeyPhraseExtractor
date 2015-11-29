#encoding "utf-8" 
#GRAMMAR_ROOT S     

Country -> "Франция" | "Германия";
Name -> Word<h-reg2>;
NounCustom -> Country;
NounCustom -> Name;
NounCustom -> Noun;
NounCustom -> Word<gram="сокр">;

S -> Adj<gnc-agr[1]>+ NounCustom<gnc-agr[1],rt>;