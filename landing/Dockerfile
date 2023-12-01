FROM node:21.2-alpine3.18

RUN mkdir -p /landing

WORKDIR /landing

COPY ./package*.json ./

RUN npm install

# COPY next.config.js ./next.config.js
# COPY tailwind.config.js ./tailwind.config.js
# COPY postcss.config.js ./postcss.config.js

# COPY app ./app
# COPY .env.local .

# RUN chmod 600 .env.local

COPY . /landing

EXPOSE 3000

CMD [ "npm", "run", "dev"]