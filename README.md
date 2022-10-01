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
