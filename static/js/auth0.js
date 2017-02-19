var lock = new Auth0Lock('sQLcidME4R6z1UdBtYB0V4ay9pwDRoML', 'udacity-itemcatalog.auth0.com', {
auth: {
    redirectUrl: 'http://localhost:3000/callback',
    responseType: 'code',
    params: {
    scope: 'openid email' // Learn about scopes: https://auth0.com/docs/scopes
    }
}
});