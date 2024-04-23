FROM node:21-alpine

WORKDIR /app

COPY . /app

RUN npm install

CMD if [ ${NODE_ENV} = "dev" ]; then npm run dev; else npm run build && npm run start; fi
