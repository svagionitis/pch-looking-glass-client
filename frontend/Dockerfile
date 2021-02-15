FROM nginx:latest

COPY ixp.html /usr/share/nginx/html/
COPY media/ /usr/share/nginx/html/media/
COPY resources/ /usr/share/nginx/html/resources/

EXPOSE 80

CMD ["nginx","-g","daemon off;"]
