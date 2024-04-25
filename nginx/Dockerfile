FROM nginx:1.15-alpine

ARG ENV=dev

COPY ./$ENV /etc/nginx/conf.d
COPY ./nginx.conf /etc/nginx/nginx.conf

CMD nginx -g "daemon off;"
