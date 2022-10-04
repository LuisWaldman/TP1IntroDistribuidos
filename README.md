# Introduccion a sistemas distribuidos - TP1

## Requisitos
### Configurar PYTHONPATH

Para no tener problemas con los imports. En `~/.bashrc` agregar:

```bash
export PYTHONPATH=.:/usr/local/lib/python
```

Validación:

```bash
$ echo $PYTHONPATH
.:/usr/local/lib/python
```

### Correr linting con tox

Validar que se usa la versión 3.10 de Python:

```bash
$ python3 --version
Python 3.10.4
```

Instalar y actualizar `pip` para manejar dependencias:

```bash
apt install python-pip
# Las versiones en los repositorios de aptitude pueden estar desactializadas.
pip install pip --upgrade
```

Instalar tox:

```bash
pip install tox
```

Correr tox:

```bash
tox
```

## Servidor

El servidor consta de un sólo comando `start-server`, que permite iniciar el servidor. Para ejecutarlo:

```python
python3 src/start-server.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]
```

Pueden utilizarse distintos flags:

* [`-h` o `--help`] permite mostrar el mensaje de ayuda y detalle de los distintos flags.
* [`-v` o `--verbose` | `-q` o `--quiet`] maneja el nivel de profundidad del logging.
* [`-H` o `--host`] permite indicar el host donde se quiere levantar el servidor.
* [`-p` o `--port`] permite indicar el puerto donde se quiere levantar el servidor.
* [`-s` o `--storage`] permite indicar el directorio donde se quieren bajar los archivos.


## Cliente

El cliente cuenta con tres comandos distintos:
* `listados`: permite obtener la lista de archivos disponibles en el servidor.
* `upload`: permite subir un archivo al servidor.
* `download`: permite descargar un archivo del servidor.

Los tres comandos pueden correrse con los siguientes flags:
* [`-h` o `--help`] permite mostrar el mensaje de ayuda y detalle de los distintos flags.
* [`-v` o `--verbose` | `-q` o `--quiet`] maneja el nivel de profundidad del logging.
* [`-H` o `--host`] permite indicar el host del servidor al que se quiere enviar el comando.
* [`-p` o `--port`] permite indicar el puerto del servidor al que se quiere enviar el comando.

Además de ciertos flags adicionales según cada comando.

### upload

Este comando puede correrse de las siguientes dos formas:
```python
python3 src/upload.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]
```

Donde vemos que tenemos dos parámetros adicionales **obligatorios**:
* `-s` o `--src` para indicar la ruta al archivo que queremos subir.
* `-n` o `--name` para indicar el nombre del archivo que queremos guardar en el servidor.

### download

Este comando puede correrse de las siguientes dos formas:
```python
python3 src/download.py [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]
```
Donde vemos que tenemos dos parámetros adicionales **obligatorios**:
* `-s` o `--src` para indicar la ruta al directorio a almacenar la descarga.
* `-n` o `--name` para indicar el nombre del archivo que queremos descargar.

### listado

Este comando puede correrse de las siguientes dos formas:
```python
python3 src/listado.py [-h] [-v | -q] [-H ADDR] [-p PORT]
```


## Comcast

Descargar e instalar [GO](https://go.dev/doc/install) e instalar
[comcast](https://github.com/tylertreat/comcast#installation).

```bash
PATH="$HOME/go/bin/:/usr/local/go/bin:$PATH"
comcast --device=lo --packet-loss=10% --target-addr=127.0.0.0/8 --target-proto=udp
comcast --stop
```
