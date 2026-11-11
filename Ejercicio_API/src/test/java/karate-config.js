function fn() {
  var env = karate.env;
  karate.log('karate.env configurado en:', env);
  if (!env) {
    env = 'prod';
  }

  var config = {
    baseUrl: 'https://api.demoblaze.com',
    defaultPassword: 'PasswordSeguro123!',
    // Funcion utilitaria para generar usuarios unicos dinamicamente
    generateRandomUser: function(prefix) {
      prefix = prefix || 'user_qa';
      var timestamp = new Date().getTime();
      var randomInt = Math.floor(Math.random() * 90000) + 10000;
      return prefix + '_' + timestamp + '_' + randomInt;
    }
  };

  karate.configure('connectTimeout', 10000);
  karate.configure('readTimeout', 15000);
  karate.configure('logPrettyRequest', true);
  karate.configure('logPrettyResponse', true);

  return config;
}

