FROM nginx:1.15-alpine

ARG BUILD_ENV=dev

COPY ./${BUILD_ENV} /etc/nginx/conf.d/

COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
