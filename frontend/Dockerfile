# Development Dockerfile for Next.js Frontend with Hot Reload
FROM node:latest

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run Next.js in development mode with hot reload
# Next.js dev mode automatically watches for file changes
CMD ["npm", "run", "dev"]
