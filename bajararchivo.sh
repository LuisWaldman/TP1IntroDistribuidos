directoriodownload=$HOME/archivodescarga/
directorioservidor=$HOME/archivos/
archivo="video1.mp4"

rm $directoriodownload$archivo
python3.10 src/download.py -v -n $archivo -d $directoriodownload;

md5descarga=$(md5sum $directoriodownload$archivo)
md5original=$(md5sum $directorioservidor$archivo)

md5solodescarga=${md5descarga:0:32}
md5soloorigen=${md5original:0:32}

if [ $md5solodescarga == $md5soloorigen ]
then
  echo "LOS ARCHIVOS SE TRANSMITIERON BIEN"
else
  echo "LOS ARCHIVOS SE TRANSMITIERON MAL"
fi



