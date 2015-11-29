# Tomita-KeyPhraseExtractor 
## Dependencies
###1. Tomita parser
На данный момент используется win32 версия. Для изменения исполняемого файла Томиты (например на linux версию) в файле `keyPhrases/__init__.py` изменить путь `"./grammar/tomitaparser.exe"` на желаемый
###2. beautifulsoup4
Используется для извлечения результатов работы парсера из `./temp/result.html`
##Пример
Для тестирования работы модуля следует запустить скрипт `keyphraseExtractorTest.py` 
