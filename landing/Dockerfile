FROM node:alpine

WORKDIR /landing

RUN npm install --global pm2

COPY ./package*.json ./

RUN npm install --production

COPY next.config.js ./next.config.js

COPY app ./app
COPY .env.local .

RUN chmod 600 .env.local

EXPOSE 3000

# CMD [ "pm2-runtime", "npm", "--", "start" ]

CMD [ "npm", "run", "dev"]