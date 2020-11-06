FROM node:12


# Create app directory
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8080


# If you are building your code for production
# RUN npm ci --only=production

CMD [ "npm", "start" ]