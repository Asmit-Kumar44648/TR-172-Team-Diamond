FROM node:20-alpine AS builder

WORKDIR /app

# Disable telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1

# Copy package manifests from the app directory
COPY apps/web/package*.json ./

# Install dependencies (using npm ci for consistent builds)
RUN npm ci

# Copy the rest of the web app source
COPY apps/web/ .

# Build the application
RUN npm run build

# Stage 2: Runner
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Using Next.js standalone output to keep the image slim
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Expose Next.js port
EXPOSE 3000

ENV PORT 3000
# set hostname to localhost
ENV HOSTNAME "0.0.0.0"

# server.js is created by next build when using standalone output
CMD ["node", "server.js"]
