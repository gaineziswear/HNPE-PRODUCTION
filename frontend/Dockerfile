FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps || true
COPY . .
CMD ["npm", "run", "dev"]
