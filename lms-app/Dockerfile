FROM node:alpine

WORKDIR /lms-app

# RUN npm install --global nodemon

COPY ./package*.json ./

RUN npm install

COPY next.config.js ./next.config.js
COPY tailwind.config.js ./tailwind.config.js
COPY postcss.config.js ./postcss.config.js

COPY pages ./pages
COPY public ./public
COPY styles ./styles
COPY .env.local .

RUN chmod 600 .env.local

# RUN npm run build

EXPOSE 3001

# CMD [ "pm2-runtime", "npm", "--", "start" ]

CMD ["npm", "run", "dev"]