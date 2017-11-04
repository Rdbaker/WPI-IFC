function identifyUser(user) {
  return drift.identify(
    user.id,
    {
      email: user.username + '@wpi.edu',
      name: user.full_name,
    }
  );
}


drift.on('ready',function(api, payload) {
  if(window.me === undefined) {
    $.get('/users/me').done(function(data) {
      window.me = data.me;
      identifyUser(data.me)
    });
  } else {
    identifyUser(window.me);
  }
})
