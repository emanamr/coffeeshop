

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
      url: 'fullstacktest.auth0.com', // the auth0 domain prefix
      audience: 'https://coffee-shop-api', // the audience set for the auth0 app
      clientId: '6bWcngY1zsg5B2pGJk7hgEJT06ENl98H', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
