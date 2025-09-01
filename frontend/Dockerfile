# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Установка зависимостей
COPY package*.json ./
RUN npm install

# Копируем исходники и билдим фронт
COPY . .
RUN npm run build

# Stage 2: Prepare nginx content
FROM nginx:alpine

# Копируем собранный фронт в папку nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Исправляем права, чтобы nginx мог читать файлы
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
