FROM node:20-alpine AS build

WORKDIR /app

ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_ANON_KEY

COPY package*.json ./
RUN npm install

COPY . .
RUN printf "VITE_SUPABASE_URL=%s\nVITE_SUPABASE_ANON_KEY=%s\n" "$VITE_SUPABASE_URL" "$VITE_SUPABASE_ANON_KEY" > .env.production
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
