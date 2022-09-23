# Introduccion a sistemas distribuidos - TP1

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

## Instalar pyyalm para el archivo de configuración

```bash
pip install pyyaml --upgrade
```

