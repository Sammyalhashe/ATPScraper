# base image
FROM node:12.2.0-alpine

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:/app/src/node_modules/.bin:$PATH
ENV DEV development

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install --silent
RUN npm install react-scripts@3.0.1 -g --silent
RUN npm install axios -g
RUN npm install react-router-dom -g

# start app
CMD ["npm", "start"]
