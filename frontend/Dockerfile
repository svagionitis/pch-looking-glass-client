FROM nginx:latest

ARG BACKEND_HOST
ARG BACKEND_PORT

WORKDIR /frontend
COPY ixp.html.in .
RUN sed "s/@BACKEND_HOST@:@BACKEND_PORT@/${BACKEND_HOST}:${BACKEND_PORT}/g" ixp.html.in > /usr/share/nginx/html/ixp.html

COPY media/ /usr/share/nginx/html/media/
COPY resources/ /usr/share/nginx/html/resources/

EXPOSE 80

CMD ["nginx","-g","daemon off;"]
