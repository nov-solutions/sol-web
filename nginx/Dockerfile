FROM nginx:1.15-alpine

# defaults to 'dev' if not provided
ARG BUILD_ENV=dev

# site conf
COPY ./${BUILD_ENV} /etc/nginx/conf.d/
# main conf
COPY ./nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
