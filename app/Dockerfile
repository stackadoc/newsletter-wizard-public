# Stage 1: Install all dependencies including devDependencies
FROM node:20-alpine AS development-dependencies-env
RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .

# Stage 2: Install only production dependencies
FROM node:20-alpine AS production-dependencies-env
RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --prod --frozen-lockfile

# Stage 3: Build the application
FROM node:20-alpine AS build-env
RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app
COPY --from=development-dependencies-env /app .
RUN pnpm run build

# Stage 4: Final production image
FROM node:20-alpine
ENV NODE_ENV=production
RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
COPY --from=production-dependencies-env /app/node_modules ./node_modules
COPY --from=build-env /app/build ./build
# You might need to copy other necessary files like public assets, config, etc.
# Example: COPY --from=build-env /app/public ./public

# Expose port if necessary (e.g., if it's a web server)
# EXPOSE 3000

CMD ["pnpm", "run", "start"]