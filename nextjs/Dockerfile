FROM node:21-alpine

ARG BUILD_ENV=dev
ENV BUILD_ENV=${BUILD_ENV}

WORKDIR /app

COPY . /app

# clean install
RUN npm ci

# run dev server or prod
CMD if [ "$BUILD_ENV" = "dev" ]; then \
        npm run dev; \
    else \
        npm run build && npm run start; \
    fi
