var oktaSignIn = new OktaSignIn({
    baseUrl: 'http://localhost:8000/proxy',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[org]]/oauth2/[[iss]]',
        responseType: ['code'],
        scopes: [[scopes]],
    }
});
oktaSignIn.renderEl(
    {el: '#okta-login-container'},
);
