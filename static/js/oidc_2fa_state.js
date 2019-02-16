var stateTokenParam = '[[stateToken]]';

var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[org]]/oauth2/[[iss]]',
        responseType: ['id_token', 'token'],
        scopes: [[scopes]],
    },
    stateToken: stateTokenParam,
    features: {
        router: true,
        registration: false,
        rememberMe: true,
        multiOptionalFactorEnroll: true,
        selfServiceUnlock: true,
        smsRecovery: true,
    	callRecovery: true,
    }
});
oktaSignIn.renderEl(
    {el: '#okta-login-container'},
    function (res) {
        console.log(res);
        var key = '';
        if (res[0]) {
            key = Object.keys(res[0])[0];
            oktaSignIn.tokenManager.add(key, res[0]);
        }
        if (res[1]) {
            key = Object.keys(res[1])[0];
            oktaSignIn.tokenManager.add(key, res[1]);
        }
        if (res.status === 'SUCCESS') {
            post_tokens(oktaSignIn.tokenManager.get('idToken'), oktaSignIn.tokenManager.get('accessToken'));
        }
    }
);
