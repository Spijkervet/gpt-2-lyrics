FROM node:12


# Create app directory
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install

RUN yarn global add serve

COPY . .

EXPOSE 5000


# If you are building your code for production
# RUN npm ci --only=production

RUN npm build

CMD [ "serve", "-s", "-l", "tcp://0.0.0.0:5000", "build"]
