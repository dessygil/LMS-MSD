FROM nginx:1.25.4-alpine3.18

WORKDIR /nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80/tcp

CMD ["nginx", "-g", "daemon off;"]