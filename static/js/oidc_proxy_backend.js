var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]'
});
oktaSignIn.renderEl(
    {el: '#okta-login-container'},
    function (res) {
        console.log(res);
        var sessionToken = res.session.token;
        console.log('sessionToken='+sessionToken);
        $('#sessionTokenInput').val(sessionToken);
        $('#SessionTokenSubmitForm').submit();


    }
);
