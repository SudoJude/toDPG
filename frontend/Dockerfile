# Stage 1: Build the Angular application
FROM node:20-alpine as build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Create dpg4x user and group
RUN addgroup -S dpg4x && adduser -S dpg4x -G dpg4x

COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

# Permissions for Nginx content (read-only is fine, but ownership good practice)
RUN chown -R dpg4x:dpg4x /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

USER dpg4x

EXPOSE 8080

# Bypass the default entrypoint which tries to modify config
ENTRYPOINT []

CMD ["nginx", "-g", "daemon off;"]
