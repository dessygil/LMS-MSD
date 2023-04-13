FROM node:alpine

WORKDIR /lms-app

RUN npm install --global pm2

COPY ./package*.json ./

RUN npm install --production

COPY next.config.js ./next.config.js

COPY pages ./pages
COPY public ./public
COPY styles ./styles
COPY .env.local .

RUN chmod 600 .env.local

# RUN npm run build

EXPOSE 3001

# CMD [ "pm2-runtime", "npm", "--", "start" ]

CMD [ "npm", "run", "dev"]

# FROM node:18-alpine AS deps
# RUN apk add --no-cache libc6-compat
# WORKDIR /lms-app

# COPY ./package*.json ./
# RUN  npm install --production

# FROM node:18-alpine AS builder
# WORKDIR /lms-app
# COPY --from=deps /lms-app/node_modules ./node_modules
# COPY . .

# ENV NEXT_TELEMETRY_DISABLED 1

# RUN npm run build

# FROM node:18-alpine AS runner
# WORKDIR /lms-app

# ENV NODE_ENV production
# ENV NEXT_TELEMETRY_DISABLED 1

# RUN addgroup --system --gid 1001 nodejs
# RUN adduser --system --uid 1001 nextjs

# COPY --from=builder --chown=nextjs:nodejs /lms-app/.next ./.next
# COPY --from=builder /lms-app/node_modules ./node_modules
# COPY --from=builder /lms-app/package.json ./package.json

# USER nextjs

# EXPOSE 3001

# ENV PORT 3001

# CMD [ "npm", "start" ]