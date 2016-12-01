class BaseViewTest:
    def login(self, user, testapp):
        res = testapp.get('/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'example'
        return form.submit().follow()
