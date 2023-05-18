FROM node:alpine

RUN mkdir -p /lms-app

WORKDIR /lms-app

COPY ./package*.json ./

RUN npm install -g npm

# COPY next.config.js ./next.config.js
# COPY tailwind.config.js ./tailwind.config.js
# COPY postcss.config.js ./postcss.config.js

# COPY pages ./pages
# COPY public ./public
# COPY styles ./styles
# COPY .env.local .

COPY . /lms-app

EXPOSE 3001

CMD ["npm", "run", "dev"]
