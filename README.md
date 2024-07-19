# Bot para Discord, desarrollado en Python.
Se han utilizado la siguientes librerias Python (incluidas en requirements.txt)

- aiohttp==3.9.3
- aiosignal==1.3.1
- attrs==23.2.0
- certifi==2024.2.2
- charset-normalizer==3.3.2
- discord.py==2.3.2
- frozenlist==1.4.1
- idna==3.6
- multidict==6.0.5
- numpy==1.26.4
- pandas==2.2.1
- python-dateutil==2.9.0.post0
- python-dotenv==1.0.1
- pytz==2024.1
- requests==2.31.0
- six==1.16.0
- tzdata==2024.1
- urllib3==2.2.1
- yarl==1.9.4

## Como utilizarlo?

- Clonar / Descargar el contenido del repositorio.
- Create a Discord Bot [aquí](https://discord.com/developers/applications)
- Obtener su TOKEN correspondiente
- Invitar al BOT an server con las siguientes instrucciones: https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS ( Reemplazar `YOUR_APPLICATION_ID_HERE` con su application ID y reemplazar `PERMISSIONS` con los permisos requeridos por lo que el bot necesita al final de este link https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot)

1) Descargar Python 3.12[https://www.python.org]:(https://www.python.org)
2) Instalar el modulo PIP: (python.exe -m pip install --upgrade pip)
3) Activar el entorno virtual: (pip install virtualenv)
4) Instalar las librerias Python, dentro del directorio : (pip install -r requirements.txt)
5) ajustar el archivo .env donde deben actualizarse segun los datos de cada Discord Server
    # Set environment variables
    TOKEN= "MTIxNDIzOTM5ODE5MTcwMjA5Nw.GBOLRR.K2323984930fnkfnfkrn4rn3mnmds"  #Incluir el Token de Seguridad generado por el Bot.
    CHANNEL="439502384934239027" #Channel ID del canal General
    GUILD="34053490390gkfgk34t435" #Guid ID del Discord Server
6) Iniciar el BOT, posicionado en el PATH donde se descargo el codigo. Ejecutar el comando: (py .\example.py)

## Compilado con
- [Python 3.12.2](https://www.python.org/)

## Se requiere crear un archivo .env vacio e incluirse los siguientes valores
    TOKEN= "MTIxNDIzOTM5ODE5MTcwMjA5Nw.GBOLRR.K2323984930fnkfnfkrn4rn3mnmds"  
    #Incluir el Token de Seguridad generado por el Bot.
    
    CHANNEL="439502384934239027" 
    #Channel ID del canal General
    
    GUILD="34053490390gkfgk34t435" 
    #Guid ID del Discord Server