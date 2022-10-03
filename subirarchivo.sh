directorioupload="/home/luis/archivosparasubir/"
directorioservidor="/home/luis/archivos/"
archivo="videosubir.mp4"

rm $directorioservidor$archivo
python3 src/upload.py -n $archivo -d $directorioupload;

md5subida=$(md5sum $directorioupload$archivo)
md5original=$(md5sum $directorioservidor$archivo)

md5solosubida=${md5subida:0:32}
md5soloorigen=${md5original:0:32}

if [ $md5solosubida == $md5soloorigen ]
then
  echo "LOS ARCHIVOS SE TRANSMITIERON BIEN"
else
  echo "LOS ARCHIVOS SE TRANSMITIERON MAL"
fi

