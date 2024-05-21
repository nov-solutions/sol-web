FROM node:21-alpine

ARG BUILD_ENV=dev
ENV BUILD_ENV=${BUILD_ENV}

WORKDIR /app

COPY . /app

RUN npm ci

CMD if [ "$BUILD_ENV" = "dev" ]; then \
        npm run dev; \
    else \
        npm run build && npm run start; \
    fi
