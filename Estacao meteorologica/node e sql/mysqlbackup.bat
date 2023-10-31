rem Caminho para a pasta bin do servidor MySQL
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"

rem Credenciais para se conectar ao servidor MySQL
set mysql_user=root
set mysql_password=JoaoDoPaoDoce

rem Nome do arquivo de backup gerado
set backup_path=F:\New Folder\MySQL Backup
set backup_name=db_milan

rem Criação do backup
mysqldump --user=%mysql_user% --password=%mysql_password% --db_milan --routines --events --result-file="%backup_path%\%backup_name%.sql"
if %ERRORLEVEL% neq 0 (
    (echo Backup failed: error during dump creation) >> "%backup_path%\mysql_backup_log.txt"
) else (echo Backup successful) >> "%backup_path%\mysql_backup_log.txt"
