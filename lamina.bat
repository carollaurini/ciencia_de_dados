CHCP 65001
IF EXIST P:\ (
GOTO substed
)
IF EXIST %USERPROFILE%"\São João Capital\Armory Front Office - Programs" (
subst p: %USERPROFILE%"\São João Capital\Armory Front Office - Programs"
GOTO substed
)
IF EXIST %USERPROFILE%"\São João Capital\Armory Front Office - Documents\General\Programs" (
subst p: %USERPROFILE%"\São João Capital\Armory Front Office - Documents\General\Programs"
GOTO substed
)
IF EXIST %USERPROFILE%"\São João Capital\Armory Front Office - General\Programs" (
subst p: %USERPROFILE%"\São João Capital\Armory Front Office - General\Programs"
GOTO substed
)
:substed
path = p:\blpapi;p:\sjpython\scripts\;%PATH%
SET PYTHONPATH = p:\lib;p:\blpapi
call p:\sjpython\scripts\activate.bat
p:

cd p:\ciencia_de_dados\Correlacao_de_fundos\LaminaProducao

python main.py

pause
