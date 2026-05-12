FROM node:20-alpine AS build

WORKDIR /app

ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_ANON_KEY
ARG VITE_API_URL
ARG VITE_PUBLIC_APP_URL=

COPY package*.json ./
RUN npm install

COPY . .
RUN printf "VITE_SUPABASE_URL=%s\nVITE_SUPABASE_ANON_KEY=%s\nVITE_API_URL=%s\nVITE_PUBLIC_APP_URL=%s\n" "$VITE_SUPABASE_URL" "$VITE_SUPABASE_ANON_KEY" "$VITE_API_URL" "$VITE_PUBLIC_APP_URL" > .env.production
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
# Bump image: trigger Railway rebuild (2026-05-12)
CMD ["nginx", "-g", "daemon off;"]
