# Introduccion a sistemas distribuidos - TP1

## Configurar PYTHONPATH

Para no tener problemas con los imports. En `~/.bashrc` agregar:

```bash
export PYTHONPATH=.:/usr/local/lib/python
```

Validación:

```bash
$ echo $PYTHONPATH
.:/usr/local/lib/python
```

## Correr linting con tox

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

## Comcast

Descargar e instalar [GO](https://go.dev/doc/install) e instalar
[comcast](https://github.com/tylertreat/comcast#installation).

```bash
PATH="$HOME/go/bin/:/usr/local/go/bin:$PATH"
comcast --device=lo --packet-loss=10% --target-addr=127.0.0.0/8 --target-proto=udp
comcast --stop
```
