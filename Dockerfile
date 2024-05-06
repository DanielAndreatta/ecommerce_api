# Usa la imagen base de Python 3.8
FROM python:3.10

# Instala nginx y otras dependencias
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends

# Copia el archivo de configuración de Nginx dentro del contenedor
COPY nginx.default /etc/nginx/sites-available/default

# Configura los logs de Nginx para que se envíen a la salida estándar
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# Crea el directorio de la aplicación y copia los archivos
RUN mkdir -p /opt/app
COPY . /opt/app

# Establece el directorio de trabajo
WORKDIR /opt/app

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Cambia los permisos de los archivos de la aplicación
RUN chown -R www-data:www-data /opt/app

# Expone el puerto 80 para que sea accesible desde fuera del contenedor
EXPOSE 80

# Inicia el servidor usando el script start-server.sh
CMD ["/opt/app/start-server.sh"]
