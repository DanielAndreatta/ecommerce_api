# Usa la imagen base de Python 3.10
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
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/ecommerce_api
COPY requirements.txt start-server.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY . /opt/app/ecommerce_api/

# Establece el directorio de trabajo
WORKDIR /opt/app

# Instala las dependencias de Python
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

# Cambia los permisos de los archivos de la aplicación
RUN chown -R www-data:www-data /opt/app

# Expone el puerto 80 para que sea accesible desde fuera del contenedor
EXPOSE 8020
STOPSIGNAL SIGTERM

# Inicia el servidor usando el script start-server.sh
CMD ["/opt/app/start-server.sh"]
