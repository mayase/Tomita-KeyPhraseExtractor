#encoding "utf-8" 
#GRAMMAR_ROOT S     

Country -> "Франция" | "Германия";
Name -> Word<h-reg2>;
NounCustom -> Country;
NounCustom -> Name;
NounCustom -> Noun;
NounCustom -> Word<gram="сокр">;

NP -> NounCustom | NounCustom NounCustom<gram="gen"> | Adj<gnc-agr[1]>+ NounCustom<gnc-agr[1],rt>; 
NNP -> NP Prep NP;
S -> NNP;