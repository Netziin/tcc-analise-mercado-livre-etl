@echo off
REM

REM
SET PROJECT_PATH=C:\Dev\tcc - completo\TCC\TCC
SET LOGFILE="%PROJECT_PATH%\pipeline_log.txt"

REM
SET VENV_PATH=%PROJECT_PATH%\.venv\Scripts

ECHO. > %LOGFILE%
ECHO ========================================================== >> %LOGFILE%
ECHO      INICIANDO PIPELINE EM %date% %time% >> %LOGFILE%
ECHO ========================================================== >> %LOGFILE%
ECHO. >> %LOGFILE%

cd /d "%PROJECT_PATH%"

ECHO [ETAPA 1 de 4] Limpando arquivos de dados antigos... >> %LOGFILE%
del "data\*.jsonl" /Q >> %LOGFILE% 2>&1
ECHO. >> %LOGFILE%

ECHO [ETAPA 2 de 4] Executando os spiders do Scrapy... >> %LOGFILE%
 
cd "src\coleta"

ECHO    - Executando spider: celular... >> %LOGFILE%
REM
"%VENV_PATH%\scrapy.exe" crawl celular -o ..\..\data\celulares.jsonl >> %LOGFILE% 2>&1

ECHO    - Executando spider: notebook... >> %LOGFILE%
REM
"%VENV_PATH%\scrapy.exe" crawl notebook -o ..\..\data\notebooks.jsonl >> %LOGFILE% 2>&1

ECHO    - Executando spider: tv... >> %LOGFILE%
REM
"%VENV_PATH%\scrapy.exe" crawl tv -o ..\..\data\tvs.jsonl >> %LOGFILE% 2>&1

ECHO    - Executando spider: tablet... >> %LOGFILE%
REM 
"%VENV_PATH%\scrapy.exe" crawl tablet -o ..\..\data\tablets.jsonl >> %LOGFILE% 2>&1

ECHO    - Executando spider: webcam... >> %LOGFILE%
REM
"%VENV_PATH%\scrapy.exe" crawl webcam -o ..\..\data\webcams.jsonl >> %LOGFILE% 2>&1

ECHO. >> %LOGFILE%

ECHO [ETAPA 3 de 4] Tratando e carregando os dados para o SQL Server... >> %LOGFILE%
 
REM
"%PROJECT_PATH%\.venv\Scripts\python.exe" "%PROJECT_PATH%\src\coleta\transformLoad\main.py" >> %LOGFILE% 2>&1
ECHO. >> %LOGFILE%

ECHO [ETAPA 4 de 4] Processo finalizado. >> %LOGFILE%
ECHO ========================================================== >> %LOGFILE%