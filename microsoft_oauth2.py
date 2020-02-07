from flask import session, render_template, request, redirect, url_for
import msal
import uuid


class MSOauth2:
    def __init__(self, flask_app, app_config):
        # a reference to the main flask app's config
        self.app_config = app_config

        # add the flask app routes
        # login page
        @flask_app.route('/login')
        def login():
            session["state"] = str(uuid.uuid4())

            # generate a auth url for the user
            auth_url = self.__build_auth_url(scopes=self.app_config.SCOPE, state=session["state"])
            return redirect(auth_url)

        # redirect after login page
        @flask_app.route(self.app_config.REDIRECT_PATH)
        def authorized():
            if request.args.get('state') != session.get("state"):
                # if the user has no state value yet
                return redirect('/')  # No-OP. Goes back to Index page
            if "error" in request.args:  # Authentication/Authorization failure
                # of tje auth request has an error
                return render_template("auth_error.html", result=request.args)
            if request.args.get('code'):
                cache = self.__load_cache()
                result = self.__build_msal_app(cache=cache).acquire_token_by_authorization_code(
                    request.args['code'],
                    scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
                    redirect_uri=url_for("authorized", _external=True))
                if "error" in result:
                    return render_template("auth_error.html", result=result)
                session["user"] = result.get("id_token_claims")
                self.__save_cache(cache)
            return redirect('/')

        # logout page
        @flask_app.route("/logout")
        def logout():
            session.clear()  # Wipe out user and its token cache from session
            return redirect(  # Also logout from your tenant's web session
                app_config.AUTHORITY + "/oauth2/v2.0/logout" +
                "?post_logout_redirect_uri=" + url_for("index", _external=True))
        return

    # get the users cache from their session
    @staticmethod
    def __load_cache():
        # create cache object
        cache = msal.SerializableTokenCache()

        # load the cache if it exists
        if session.get("token_cache"):
            cache.deserialize(session["token_cache"])

        return cache

    # save a cache to the users session
    @staticmethod
    def __save_cache(cache):
        # only save the cache if the state has changed
        if cache.has_state_changed:
            session["token_cache"] = cache.serialize()

    # build a msal client app
    def __build_msal_app(self, cache=None, authority=None):
        return msal.ConfidentialClientApplication(
            self.app_config.CLIENT_ID, authority=authority or self.app_config.AUTHORITY,
            client_credential=self.app_config.CLIENT_SECRET, token_cache=cache)

    # get the authorization url
    def __build_auth_url(self, authority=None, scopes=None, state=None):
        return self.__build_msal_app(authority=authority).get_authorization_request_url(
            scopes or [],
            state=state or str(uuid.uuid4()),
            redirect_uri=url_for("authorized", _external=True))

    # get a users token from the cache
    def __get_token_from_cache(self, scope=None):
        cache = self.__load_cache()  # This web app maintains one cache per session
        cca = self.__build_msal_app(cache=cache)
        accounts = cca.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            result = cca.acquire_token_silent(scope, account=accounts[0])
            self.__save_cache(cache)
            return result
