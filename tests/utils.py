class BaseViewTest:
    def login(self, user, testapp):
        res = testapp.get('/')
        form = res.forms['loginForm']
        form['email'] = user.email
        form['password'] = 'example'
        return form.submit().follow()
